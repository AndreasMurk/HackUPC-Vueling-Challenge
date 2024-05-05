from typing_extensions import override
from openai import AssistantEventHandler
import os
import json

# Get the absolute path to the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
tools_file_path = os.path.join(current_dir, 'tools.json')


class Assistant:
    def __init__(self, client):
        self.client = client
        with open(tools_file_path) as f:
            tools = json.load(f)
        self.assistant = client.beta.assistants.create(
            name="Airport Assistant",
            instructions="You are an airport assistant for visually impaired people. Answer questions about the airport process. The airport process consist of the following: Check-In, Baggage Information, Security Instructions, and Boarding information.",
            tools=tools,
            model="gpt-4-turbo"
        )
        self.thread = self.client.beta.threads.create()
        self.event_handler = EventHandler(self.client, self.thread)

    def receive_message(self, message):
        message_obj = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

        with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
                event_handler=self.event_handler
        ) as stream:
            stream.until_done()

        return self.event_handler.get_last_response()


class EventHandler(AssistantEventHandler):
    def __init__(self, client, thread):
        super().__init__()
        self.responses = []
        self.client = client
        self.thread = thread

    @override
    def on_event(self, event):
        if event.event == 'thread.message.completed':
            self.responses.append(event.data.content[0].text.value)
        elif event.event == 'thread.run.requires_action':
            run_id = event.data.id
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "get_airport_name":
                tool_outputs.append({"tool_call_id": tool.id, "output": "JFK"})

        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )

    def get_last_response(self):
        return self.responses[-1] if self.responses else None
