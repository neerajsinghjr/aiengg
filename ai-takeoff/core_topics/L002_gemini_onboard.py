# --------------------------------------------------------------------------
# Raw Response: response=GenerateContentResponse(
#   automatic_function_calling_history=[],
#   candidates=[
#     Candidate(
#       content=Content(
#         parts=[
#           Part(
#             text="""Hey there!
#
# Not much happening on my end, just processing information and ready to chat!
#
# What's on your mind? How can I help you today?"""
#           ),
#         ],
#         role='model'
#       ),
#       finish_reason=<FinishReason.STOP: 'STOP'>,
#       index=0
#     ),
#   ],
#   model_version='gemini-2.5-flash',
#   response_id='Qw6TacSnCZj6juMPt93gyAo',
#   sdk_http_response=HttpResponse(
#     headers=<dict len=11>
#   ),
#   usage_metadata=GenerateContentResponseUsageMetadata(
#     candidates_token_count=34,
#     prompt_token_count=8,
#     prompt_tokens_details=[
#       ModalityTokenCount(
#         modality=<MediaModality.TEXT: 'TEXT'>,
#         token_count=8
#       ),
#     ],
#     thoughts_token_count=765,
#     total_token_count=807
#   )
# )
#
# response.text="Hey there!\n\nNot much happening on my end, just processing
# information and ready to chat!\n\nWhat's on your mind? How can I help you today?"
# ---------------------------------------------------------------------------

from dotenv import load_dotenv, find_dotenv
from google import genai
from os import environ as env

load_dotenv(find_dotenv())

client = genai.Client()

response = client.models.generate_content(
    model=env.get("GEMINI_MODEL"),
    contents="Hi There, Whats Happening ?"
)

print(f"{response.text=}")