import json
import logging
import random
import re
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

logger = logging.getLogger(__name__)

class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        return [SessionStarted()]

class ActionAssignCondition(Action):
    def name(self) -> Text:
        return "action_assign_condition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the call metadata from the tracker as raw text
        raw_text = tracker.latest_message.get('text', "")
        logger.info(f"Raw metadata: {raw_text}")
        # Default condition and user id
        condition = "1"
        user_id = "unknown"

        conditions = [
            "emp_gs",
            "emp_gn",
            "neu_gs",
            "neu_gn"
        ]

        try:
            # Extract JSON part (everything from first '{' to end)
            # e.g. "/trigger_flow{\"flow\": \"welcome\", \"metadata\": {\"condition\":\"1\",\"user_id\":\"123\"}}"
            json_match = re.search(r'\{.*\}', raw_text)

            if json_match:
                json_string = json_match.group(0)
                # Parse string into a Python dict
                data = json.loads(json_string)

                # Access nested metadata
                metadata = data.get("metadata", {})
                condition = metadata.get("condition", "1")
                user_id = metadata.get("user_id", "unknown")

                logger.info(f"Condition: {condition}, User: {user_id}")

        except Exception as e:
            logger.info(f"Error while extracting metadata: {e} ---")
            # Random assignment in error case
            selected_condition = random.choice(conditions)
            logger.info(f"User assigned to condition: {selected_condition}")
            return [
                SlotSet("linguistic_condition", selected_condition),
                SlotSet("user_id", user_id)
            ]

        selected_condition = conditions[int(condition) - 1]
        logger.info(f"User assigned to condition: {selected_condition}")

        return [
            SlotSet("linguistic_condition", selected_condition),
            SlotSet("user_id", user_id)
        ]

class ActionSetUserNameEmp(Action):
    def name(self) -> Text:
        return "action_set_user_name_emp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        condition = tracker.get_slot("linguistic_condition")
        if condition == "emp_gs":
            emp_name = tracker.get_slot("user_name_emp_gs")
            logger.info(f"User emp name: {emp_name}")
            return [SlotSet("user_name", emp_name)]
        else: #emp_gn
            emp_name = tracker.get_slot("user_name_emp_gn")
            logger.info(f"User emp name: {emp_name}")
            return [SlotSet("user_name", emp_name)]


class ActionSetUserNameNeu(Action):
    def name(self) -> Text:
        return "action_set_user_name_neu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        condition = tracker.get_slot("linguistic_condition")
        if condition == "neu_gs":
            neu_name = tracker.get_slot("user_name_neu_gs")
            logger.info(f"User neu name: {neu_name}")
            return [SlotSet("user_name", neu_name)]
        else: #neu_gn
            neu_name = tracker.get_slot("user_name_neu_gn")
            logger.info(f"User neu name: {neu_name}")
            return [SlotSet("user_name", neu_name)]


class ActionGenderTitleEmp(Action):
    def name(self) -> Text:
        return "action_fill_gender_title_emp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text")
        logger.info(f"Latest user message: {user_message}")

        val = str(user_message).lower().replace(".", "").strip()

        logger.info(f"Gender value: {val}")

        # Possible input values
        mr = ["mr", "mister", "sir", "man"]
        ms = ["ms", "miss", "madam", "lady", "mrs"]

        if any(s in val for s in ms):
            return [SlotSet("gender_title_emp", "Ms.")]
        elif any(m in val for m in mr):
            return [SlotSet("gender_title_emp", "Mr.")]
        else:
            return [SlotSet("gender_title_emp", None)]

class ActionGenderTitleNeu(Action):
    def name(self) -> Text:
        return "action_fill_gender_title_neu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text")
        logger.info(f"Latest user message: {user_message}")

        val = str(user_message).lower().replace(".", "").strip()
        logger.info(f"Gender value: {val}")

        # Possible input values
        mr = ["mr", "mister", "sir", "man"]
        ms = ["ms", "miss", "madam", "lady", "mrs"]

        if any(s in val for s in ms):
            return [SlotSet("gender_title_neu", "Ms.")]
        elif any(m in val for m in mr):
            return [SlotSet("gender_title_neu", "Mr.")]
        else:
            return [SlotSet("gender_title_neu", None)]

class ActionFillUserAnswerEmp(Action):
    def name(self) -> Text:
        return "action_fill_user_answer_emp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text")

        logger.info(f"Latest user message (emp): {user_message}")
        return [SlotSet("user_answer_emp", user_message)]


class ActionFillUserAnswerNeu(Action):
    def name(self) -> Text:
        return "action_fill_user_answer_neu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text")

        logger.info(f"Latest user message (neu): {user_message}")
        return [SlotSet("user_answer_neu", user_message)]

class ActionEvaluateUserAnswer(Action):
    def name(self) -> Text:
        return "action_evaluate_user_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        condition = tracker.get_slot("linguistic_condition")

        if condition == "emp_gs" or condition == "emp_gn":
            user_message = tracker.get_slot("user_answer_emp")
        elif condition == "neu_gs" or condition == "neu_gn":
            user_message = tracker.get_slot("user_answer_neu")
        else:
            user_message = tracker.get_slot("user_answer_neu")

        # Validate user message before evaluating
        if ";" not in user_message:
            if "emp_gs" in (condition or "") or "emp_gn" in (condition or ""):
                dispatcher.utter_message(
                    text="Oops! It looks like the semicolons are missing. Could you try sending that again using the '［gap＿1］; ... ; ［gap＿6］' format?")
            else: # Neutral conditions
                dispatcher.utter_message(text="Invalid format. Provide the answer using the required ';' separators.")
            return [SlotSet("answer_format_error", True)]

        semicolon_count = user_message.count(";")

        # Fewer semicolons
        if semicolon_count < 5:
            if "emp_gs" in (condition or "") or "emp_gn" in (condition or ""):
                dispatcher.utter_message(
                    text="Oops! It looks like a few semicolons are missing! Remember to use the '［gap＿1］; ... ; ［gap＿6］' format so I can check your solution.")
            else:
                dispatcher.utter_message(
                    text="Format Error: Incorrect number of separators. 5 semicolons required for 6 input slots.")
            return [SlotSet("answer_format_error", True)]

        # More semicolons than required
        if semicolon_count >= 6:
            if "emp_gs" in (condition or "") or "emp_gn" in (condition or ""):
                dispatcher.utter_message(
                    text="Oops! It looks like you've used a few more semicolons! Remember to use the '［gap＿1］; ... ; ［gap＿6］' format so I can check your solution.")
            else:
                dispatcher.utter_message(
                    text="Format Error: Incorrect number of separators. 5 semicolons required for 6 input slots.")
            return [SlotSet("answer_format_error", True)]

        # Extract user answers and remove all unnecessary whitespaces inbetween + everything in lowercase
        user_ans_array = ["".join(item.split()).lower() for item in user_message.split(";")]
        logger.info(f"validate user array all: {user_ans_array}")

        no_wrong_slot = 0
        which_slots_were_wrong = []

        user_level = tracker.slots.get("user_level")
        logger.info(f"validate user level: {user_level}")
        if user_level == "low":
            sol = ['src', 'aux', 'dst', 'aux', 'dst', 'src']
        elif user_level == "med":
            sol = ['(n-1)', 'aux', 'dst', '(n-1)', 'aux', 'src']
        elif user_level == "high":
            sol = ['n', '1', 'toh((n-1),src,aux,dst)', 'src', 'dst', 'toh((n-1),aux,dst,src)']
        else: # No level assigned (error case)
            sol = ['(n-1)', 'aux', 'dst', '(n-1)', 'aux', 'src']

        for i in range(len(sol)):
            if sol[i] != user_ans_array[i]:
                # Allow answers without brackets
                if sol[i] == '(n-1)' and user_ans_array[i] == 'n-1':
                    continue
                if sol[i] == 'toh((n-1),src,aux,dst)' and user_ans_array[i] == 'toh(n-1,src,aux,dst)':
                    continue
                if sol[i] == 'toh((n-1),aux,dst,src)' and user_ans_array[i] == 'toh(n-1,aux,dst,src)':
                    continue
                no_wrong_slot += 1
                which_slots_were_wrong.append(i+1)

        string_which_slots_were_wrong = ", ".join([str(x) for x in which_slots_were_wrong])

        logger.info(f" Number of wrong slots: {no_wrong_slot}")
        logger.info(f" Which slots were wrong: {string_which_slots_were_wrong}")

        return [SlotSet("answer_format_error", False),
                SlotSet("number_wrong_slot", no_wrong_slot),
                SlotSet("which_slots_were_wrong", string_which_slots_were_wrong)]

class ActionFillEvaluationNeu(Action):
    def name(self) -> Text:
        return "action_fill_evaluation_neu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text")

        logger.info(f"Latest user message (neu): {user_message}")
        return [SlotSet("evaluation_neu", user_message)]
