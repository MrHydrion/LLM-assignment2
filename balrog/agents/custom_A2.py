import copy
import re
import sys

from balrog.agents.base import BaseAgent
from collections import deque



class CustomAgent(BaseAgent):
    """An agent that generates actions and plans based on observations with a customizable approach."""

    def __init__(self, client_factory, prompt_builder):
        super().__init__(client_factory, prompt_builder)
        self.client = client_factory()
        # self.plan = None
        self.ActionMemory = deque(maxlen=10)
        self.step_count = 0 # for debugging

    def act(self, obs, prev_action=None):
        """Generate the next action and update the plan based on the current observation.

        Args:
            obs (dict): The current observation in the environment.
            prev_action (str, optional): The previous action taken.

        Returns:
            LLMResponse: The response containing the updated plan and selected action.
        """

        repitition = 0
        faulty_actions = []

        if prev_action:
            self.prompt_builder.update_action(prev_action)

            long_term = obs["text"].get("long_term_context", "")

            invalid = "Your previous output did not contain a valid action" in long_term

            if invalid and "\n\nObservation:\n" in long_term:
                long_term = long_term.split("\n\nObservation:\n", 1)[1]

            # save what was done before
            self.ActionMemory.append({
                "action": prev_action,
                "long_term": long_term,
                "short_term": obs["text"].get('short_term_context', ""),
                "invalid": invalid
            })

            # cant find loops if there is no memory
            if len(self.ActionMemory) >= 2:
                repitition, faulty_actions = self.detect_repitition()

                if repitition != 0:
                    print(
                        f"\nLOOP DETECTED: type={repitition}, "
                        f"actions={faulty_actions}",
                        flush=True
                    )


        if repitition == 0:
            warning = None

        elif repitition == 1:
            warning = (
                f"The action '{faulty_actions[-1]}' was repeated without changing "
                "the observation. Repeating it again is unlikely to help. "
                "Choose a different valid action that may change the situation."
            )

        elif repitition == 2:
            warning = (
                f"The action sequence {faulty_actions} is repeating without progress. "
                "Break this cycle by choosing an action outside this sequence "
                "that helps achieve the objective."
            )

        elif repitition == 3:
            warning = (
                f"The action '{faulty_actions[-1]}' has repeatedly been invalid. "
                "Choose another action from the available valid actions."
            )

        elif repitition == 4:
            warning = (
                f"The recent actions {faulty_actions} have not changed the observation. "
                "Avoid repeating this ineffective sequence. "
                "Choose an alternative action based on your current surroundings."
            )

               
        self.prompt_builder.update_observation(obs)

#         plan_text = f"Current Plan:\n{self.plan}\n" if self.plan else "You have no plan yet.\n"

#         planning_instructions = """
# Review the current plan above if present. Decide whether to continue with it or make changes.
# If you make changes, provide the updated plan. Then, provide the next action to take.
# You must output an action at every step.
# Format your answer in the following way:
# PLAN: <your updated plan if changed, or "No changes to the plan." if the current plan is good>
# ACTION: <your next action>
#         """.strip()

        messages = self.prompt_builder.get_prompt()
        naive_instruction = (
            "You always have to output one of the above actions at a time "
            "and no other text. You always have to output an action "
            "until the episode terminates."
        )

        if messages and messages[-1].role == "user":
            messages[-1].content += "\n\n" + naive_instruction
            if warning:
                messages[-1].content += "\n\n" + warning 


        response = self.client.generate(messages)

        # might delete later *sinc eadded while raging
        if warning:
            selected_action = self._extract_final_answer(response).completion.strip()

            warning_sent = (
                bool(messages)
                and messages[-1].role == "user"
                and warning in messages[-1].content
            )

            print(
                f"FEEDBACK TEST | Step {self.step_count + 1} | "
                f"Warning sent: {warning_sent} | "
                f"Type: {repitition} | "
                f"Previous: {prev_action} | "
                f"Selected: {selected_action} | "
                f"Changed: {selected_action != prev_action}",
                flush=True
            )

        # Extract the plan and action from the LLM's response
        # plan, action = self._extract_plan_and_action(response.completion)

        # # Update the internal plan if it has changed
        # if plan != "No changes to the plan.":
        #     self.plan = plan

        # # Save the plan in the response.reasoning field and the action in response.completion
        # response = response._replace(reasoning=plan, completion=action)

        self.step_count += 1

        # print(f"\n--- OBSERVATION DEBUG (Episode Step {self.step_count} ---")
        # print("Previous action:", prev_action)
        # print("Long-term context:", repr(obs["text"].get("long_term_context", "")))
        # print("Short-term context:", repr(obs["text"].get("short_term_context", "")))
  

        if repitition != 0:
            print(
                f"LOOP DETECTED: type={repitition}, "
                f"action={prev_action}, warning={warning}",
                flush=True
            )

        return self._extract_final_answer(response)


    def _extract_final_answer(self, answer):
            """Sanitize the final answer, keeping only alphabetic characters.
    
            Args:
                answer (LLMResponse): The response from the LLM.
    
            Returns:
                LLMResponse: The sanitized response.
            """
    
            def filter_letters(input_string):
                return re.sub(r"[^a-zA-Z\s:]", "", input_string)
    
            final_answer = copy.deepcopy(answer)
            final_answer = final_answer._replace(completion=filter_letters(final_answer.completion))
    
            return final_answer

    

    def _extract_plan_and_action(self, response_text):
        """Extract the plan and action from the LLM's response text.

        Args:
            response_text (str): The response text from the LLM.

        Returns:
            tuple: A tuple containing the extracted plan and action.
        """
        plan_match = re.search(r"PLAN:\s*(.*?)(?=\nACTION:|\Z)", response_text, re.IGNORECASE | re.DOTALL)
        action_match = re.search(r"ACTION:\s*(.*)", response_text, re.IGNORECASE | re.DOTALL)

        plan = plan_match.group(1).strip() if plan_match else "No changes to the plan."
        action = action_match.group(1).strip() if action_match else None

        return plan, action

    
    def detect_repitition(self):
        """
        Detect repeated actions and repeated observations in the memory
        """
        memory = list(self.ActionMemory)
        last_2_actions = memory[-2:]
        last_3_actions = memory[-3:]
        last_4_actions = memory[-4:]

        
        
        # senario where the same action that is invalid is done
        # "collect stone, collect stone" when there is no stone to collect
        if (
            last_2_actions[0]["invalid"]
            and last_2_actions[1]["invalid"]
            and last_2_actions[0]["action"] == last_2_actions[1]["action"]
        ):
            return 3, [last_2_actions[0]["action"]]

        # First senario: if the last 3 actions were the same and didnt have any progress, it is a 
        # senario: Forward, Forward, Forward (with the same observation)
        
        if (
            all(
                action["action"] == last_2_actions[0]["action"]
                for action in last_2_actions
            )
            and all(
                obs["long_term"] == last_2_actions[0]["long_term"]
                and obs["short_term"] == last_2_actions[0]["short_term"]
                for obs in last_2_actions
            )
        ):  
            return 1, [actions["action"] for actions in last_2_actions]

        # if the last 4 actions have repeating actions with the same observations and no progression.
        # senario: Left, Right, Left, Right (with both left having the same observation and b)
        if len(memory) >= 4:
            if (
                last_4_actions[0] == last_4_actions[2]
                and last_4_actions[1] == last_4_actions[3]
                and last_4_actions[0] != last_4_actions[1]
            ):
                return 2, [last_4_actions[0]["action"], last_4_actions[1]["action"]]
        
        # detiction of when 3 
        # right forward drop all having the same observations
        if len(memory) >= 3:
            if all(
                obs["long_term"] == last_3_actions[0]["long_term"]
                and obs["short_term"] == last_3_actions[0]["short_term"]
                for obs in last_3_actions
            ):
                return 4, [actions["action"] for actions in last_3_actions]

        # return 0 if no strange case
        return 0, []

    def reset(self):
        """Clear short-term memory at the start of each episode."""
        super().reset()
        self.ActionMemory.clear()
        self.step_count = 0