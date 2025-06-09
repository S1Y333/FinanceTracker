from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FilePurpose, MessageAttachment, FileSearchTool
from azure.identity import DefaultAzureCredential
import time

class SpendingAdvisorAI:
    def __init__(self, project_connection_string, agent_id):
        self.client = AIProjectClient.from_connection_string(
            project_connection_string, credential=DefaultAzureCredential()
        )
        self.agent_id = agent_id   
        # print("success - AI Client initialized with agent ID:", self.agent_id)

    # this method formats the records and sends them to the AI agent for advice
    def get_advice_from_records(self, records):
        """Format records and get advice from AI."""
        if not records:
            return "No records to analyze. Please add some records first."
        # print("success - Records received for advice:", records)
        summary = "\n".join([f"{cat} - {subcat}: ${amt}" for cat, subcat, amt in records])
        
        prompt = (
            "Based on the following spending and income records, provide advice on how to improve saving habits and reduce unnecessary expenses:\n"
            f"{summary}"
        )
        thread = self.client.agents.create_thread()
        print(f"Created thread, thread ID: {thread.id}")

        self.client.agents.create_message(
            thread_id=thread.id, role="user", content=prompt
        )

         # Process the request
        self.client.agents.create_and_process_run(thread_id=thread.id, agent_id=self.agent_id)
        

        messages = self.client.agents.list_messages(thread_id=thread.id)
            
            # Look for the assistant's reply
        for msg in messages["data"]:
            if msg["role"] == "assistant":
                response_content = msg["content"][0]["text"]["value"]
                return response_content

        return "AI did not respond in time. Please try again."
      

        

    

