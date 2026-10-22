
import copy
import re
from balrog.agents.base import BaseAgent


class CustomA3Agent(BaseAgent):
    """A general Reflexion agent with natural-language episodic memory."""


    def __init__(self, client_factory, prompt_builder):
        super().__init__(client_factory, prompt_builder)

        # Lessons learned from previous experience in the current episode.
        self.reflection_memory = []
        self.max_memory_size = 5

        # keep the observation from the preceding decision for self-reflection.
        self.previous_observation = None



    def act(self, obs, prev_action=None):
        """Reflect on previous experience, update memory, and select an action."""

        # update the conversation
        if prev_action:
            self.prompt_builder.update_action(prev_action)

        self.prompt_builder.update_observation(obs)
        messages = copy.deepcopy(self.prompt_builder.get_prompt())
        reflection_text = ""

        # reflect on perevious action, first decision no prior to reflect on
        if prev_action is not None and self.previous_observation is not None:

            reflection_text = self.reflect(previous_observation=self.previous_observation, previous_action=prev_action, current_observation=obs, messages=messages)
            lesson = self.extract_field(reflection_text, "LESSON")

            if lesson:
                self.remember_lesson(lesson)

        # the original task prompt plus the lessons learned so far
        action_messages = copy.deepcopy(messages)
        memory_text = self.format_memory()

        # reflection to tell the model how to choose an action
        reflexion_instructions = f"""
        You are an agent that must achieve the objective specified in the task.

        You can use your previous experience and a short memory of lessons
        learned from earlier decisions.

        LESSON MEMORY:
        {memory_text}

        Before choosing your next action, evaluate the previous outcome:

        1. OBJECTIVE: 
            Identify the task objective and what would count as observable progress towards it.

        2. LAST OUTCOME: 
            Compare the previous observation with the current observation. 
            Determine whether the previous action appears to have resulted in PROGRESS, NO PROGRESS, a SETBACK, or was it UNCLEAR.

        3. LESSON SELECTION: 
            Use a stored lesson only if the current evidence makes it relevant. 
            Explain briefly how it changes your decision.
            Do not force a connection to an irrelevant lesson.

        4. PLAN REVISION: 
            If the previous action did not produce the intended progress, reconsider the approach. 
            Identify what assumption or choice may have been ineffective, and select a meaningfully different action when the available evidence supports doing so.

            Do not repeat an ineffective action simply because it was part of the previous plan. 
            However, repeating an action can be reasonable when the situation or objective justifies it.

        5. ACTION: 
            Select exactly one action permitted by the task prompt.
            Base the choice on the objective, current evidence, and relevant experience. 
            Do not invent observations, capabilities, or actions.

        Be explicit about uncertainty. 
        A lack of observed progress does not always prove that an action failed, and a change in the environment does not always mean that the agent caused it.
        Keep your assessment concise and make the decision specific. 
        Avoid repeating generic advice without explaining how it affects the action.

        Output your response in this format:

        ASSESSMENT: <current evidence and progress towards the objective>
        LAST OUTCOME: <what the previous action appears to have achieved>
        LESSON USED: <relevant lesson and its application, or None>
        PLAN REVISION: <what should change, or why the current approach remains appropriate>
        ACTION: <exactly one permitted action>
        """.strip()


        if action_messages and action_messages[-1].role == "user":
            action_messages[-1].content += ("\n\n" + reflexion_instructions)

        # get the action from the llm
        response = self.client.generate(action_messages)
        action = self.extract_action(response.completion)
        self.previous_observation = copy.deepcopy(obs)

        reasoning_parts = []

        if reflection_text:
            reasoning_parts.append("REFLECTION:\n" + reflection_text)

        reasoning_parts.append("ACTION REASONING:\n" + response.completion)

        return response._replace(completion=action, reasoning="\n\n".join(reasoning_parts))



    def reflect(self, previous_observation, previous_action, current_observation, messages):
        """Evaluate a previous transition and propose a reusable lesson."""

        previous_text = self.format_observation(previous_observation)
        current_text = self.format_observation(current_observation)
        memory_text = self.format_memory()

        # prompt reflecting on the action
        reflection_prompt = f"""
        You are the reflection component of a general-purpose Reflexion agent.
        Your goal is to learn from the result of the agent's previous action and produce a useful lesson that can improve future decisions.

        PREVIOUS OBSERVATION:
        {previous_text}

        ACTION TAKEN:
        {previous_action}

        CURRENT OBSERVATION:
        {current_text}

        EXISTING LESSONS:
        {memory_text}

        Analyze the transition in the following order:

        1. EVIDENCE: 
            Identify the meaningful differences between the previous and current observations. 
            Distinguish actual changes from details that stayed the same. 
            Do not invent missing information.

        2. OUTCOME: 
            Compare the observed result with the task objective and the apparent purpose of the previous action. 
            Did the result indicate PROGRESS, NO PROGRESS, a SETBACK, or was it UNCLEAR.

        3. CAUSALITY: 
            Assess whether the previous action plausibly contributed to the observed result. 
            Do not automatically attribute every change to the action. 
            Other factors may have influenced the result.

        4. LEARNING: 
            Identify a specific adjustment that could improve a future decision in a similar situation. 
            Explain when that adjustment applies and what the agent should do differently.

        A useful lesson should be actionable. 
        The lesson must be supported by the available evidence. 
        Do not turn uncertainty into a fact, infer hidden mechanics without evidence, or generalize too strongly from one transition.

        Do not produce generic advice such as:
        - Always assess the environment carefully.
        - Consider the overall situation.
        - Actions have consequences.
        - Gather more information before deciding.

        Such advice is insufficient unless it specifies what information matters and how that information should change the decision.
        Do not force a lesson from every transition. 
        If the observations do not support a useful decision adjustment, write LESSON: None.
        Avoid repeating existing lessons. 
        If a new transition supports an important refinement of an existing lesson, provide the more specific version instead.

        Output exactly these fields:

        EVIDENCE: <important changes, or no meaningful change observed>
        OUTCOME: <progress, no clear progress, setback, or uncertain, with reason>
        CAUSALITY: <how strongly the action plausibly contributed, and why>
        REFLECTION: <brief interpretation of what was learned>
        LESSON: <one concise, actionable lesson, or None>
        """.strip()


        reflection_messages = copy.deepcopy(messages)

        if reflection_messages and reflection_messages[-1].role == "user":
            reflection_messages[-1].content += ("\n\n" + reflection_prompt)
        else:
            return ""

        response = self.client.generate(reflection_messages)
        reflection = response.completion.strip()
        
        return reflection



    def remember_lesson(self, lesson):
        """Store concise, actionable lessons without accumulating duplicates."""

        if not lesson:
            return

        lesson = re.sub(r"\s+", " ", lesson).strip()

        # no lesson, not usefull
        if not lesson or lesson.lower() in {
            "none", 
            "n/a", 
            "no lesson", 
            "no useful lesson"
            }:
            return

        normalized = self.normalize_text(lesson)

        # lessons that dont say anything are not usefull
        generic_lessons = {
            "actions have consequences",
            "consider the overall situation",
            "consider the overall direction and context",
            "assess the environment carefully",
            "gather more information before deciding",
            "always assess the environment more thoroughly before taking a decision",
        }

        if normalized in generic_lessons:
            return

        # add usefull new lessons
        for index, existing in enumerate(self.reflection_memory):
            if self.normalize_text(existing) == normalized:
                return

        self.reflection_memory.append(lesson)
        self.reflection_memory = self.reflection_memory[-self.max_memory_size:]



    def format_memory(self):
        """Format memory for the prompt."""

        if not self.reflection_memory:
            return "No lessons have been learned yet."

        return "\n".join(
            f"{index}. {lesson}"
            for index, lesson in enumerate(self.reflection_memory, start=1)
        )



    def format_observation(self, obs):
        """Convert an observation into readable text for reflection."""

        if isinstance(obs, dict):
            text = obs.get("text")

            if isinstance(text, dict):
                parts = []

                for key, value in text.items():
                    if value:
                        parts.append(f"{key}: {value}")

                if parts:
                    return "\n".join(parts)

            if isinstance(text, str) and text.strip():
                return text

        return str(obs)



    def extract_field(self, text, field):
        """Extract a named field from a structured LLM response."""

        match = re.search(
            rf"^\s*{re.escape(field)}\s*:\s*(.*?)(?=^\s*[A-Z][A-Z _-]*\s*:|\Z)",
            text,
            re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )

        if not match:
            return None

        value = match.group(1).strip()

        if not value or value.lower() in {
            "none",
            "n/a",
            "no lesson",
        }:
            return None

        return value



    def extract_action(self, response_text):
        """Extract the selected action from the model response."""

        match = re.search(
            r"^\s*ACTION\s*:\s*(.+?)\s*$",
            response_text,
            re.IGNORECASE | re.MULTILINE,
        )

        if match:
            return match.group(1).strip()

        return response_text.strip()



    def normalize_text(self, text):
        """Normalize text for duplicate comparison."""

        return re.sub(r"\s+", " ", text.strip().lower())



    def reset(self):
        """Clear the agent's episodic memory and prompt history."""

        super().reset()
        self.reflection_memory.clear()
        self.previous_observation = None
