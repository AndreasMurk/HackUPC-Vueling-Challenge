from typing_extensions import override
from openai import AssistantEventHandler


class Assistant:
    def __init__(self, client):
        self.client = client
        self.assistant = client.beta.assistants.create(
            name="Airport Assistant",
            instructions="You are an airport assistant for visually impaired people. Answer questions about the airport process",
            tools=[{
                "type": "function",
                "function": {
                    "name": "get_airport_name",
                    "description": "Get the name of the airport closest to the given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g., San Francisco, CA"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }],
            model="gpt-4-turbo"
        )
        self.thread = self.client.beta.threads.create()
        self.event_handler = EventHandler()

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
    def __init__(self):
        super().__init__()
        self.responses = []

    @override
    def on_event(self, event):
        print(f"Event received: {event}")  # Debug print to observe events
        #import pdb; pdb.set_trace()
        if event.event == 'thread.message.completed':
            print(f"Message event: {event.data.content[0].text.value}")  # Debug print for message contents
            self.responses.append(event.data.content[0].text.value)
        elif event.event == 'thread.run.requires_action':
            print(f"Requires action: {event.data}")  # Debug print for actions needed
            run_id = event.data['id']
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data['required_action']['submit_tool_outputs']['tool_calls']:
            if tool['function']['name'] == "get_airport_name":
                tool_outputs.append({"tool_call_id": tool['id'], "output": "JFK"})

        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )

    def get_last_response(self):
        return self.responses[-1] if self.responses else None
