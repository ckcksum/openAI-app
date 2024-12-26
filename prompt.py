class Prompt:
    def __init__(self):
        self.general_prompt = (
            "As an AI assistant, your task is to improve the English of the text or vocabulary I provide. Please do not highlight the mistakes; simply offer a corrected version. Ensure that the original meaning of the text is retained, and try to preserve the original wording as much as possible, unless it is unclear or contains substantial grammatical errors."
        )
        self.email_prompt = "Formal tone. No need to be professional unless specified. If subject of the email is not provided, please create one. And return the improved text in general email format"
        self.textchat_prompt = "Allow for informal language and short forms. Casual and friendly tone. No need to be professional unless specified. Return the improved text in a casual chat format."

    def get_system_prompt(self, input_type: str) -> str:
        if input_type == 'e':
            return self.general_prompt + " " + self.email_prompt
        elif input_type == 'c':
            return self.general_prompt + " " + self.textchat_prompt
        else:
            return self.general_prompt
    