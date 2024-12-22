# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import subprocess
import os
import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionExecuteEnrollFile(Action):

    def name(self) -> str:
        return "action_execute_enroll_file"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        try:

    
            dispatcher.utter_message(text="I've executed the enrollment process. To enroll you'll need your citizenship and the marksheet of your +2 . I'll turn on the camera and ask for your documents kindly place them within the rectangle to get a picture")
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "new.py"))
            subprocess.run(["python", script_path], check=True)


        except subprocess.CalledProcessError as e:
            # logging.error(f"Failed to execute loan file: {e}")
            dispatcher.utter_message(text="Failed to execute the enrollment process. Can you please provide your input again?")
        except Exception as e:
            # logging.error(f"An unexpected error occurred: {e}")
            dispatcher.utter_message(text="An unexpected error occurred while executing the enrollment process. Can you please provide your input again?")
        return []


class ActionMyDetails(Action):

    def name(selfg) -> str:
        return "actions_mydetails"

    def run(selfg, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        try:
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "detect.py"))
            subprocess.run(["python", script_path], check=True)


        except subprocess.CalledProcessError as e:
            # logging.error(f"Failed to execute loan file: {e}")
            dispatcher.utter_message(text="Failed to recognize.")
        except Exception as e:
            # logging.error(f"An unexpected error occurred: {e}")
            dispatcher.utter_message(text="An unexpected error occurred while recognizing you")
        return []