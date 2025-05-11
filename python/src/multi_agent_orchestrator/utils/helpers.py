"""
Helpers method
"""
from typing import Any
from multi_agent_orchestrator.types import ConversationMessage, TimestampedMessage

def is_tool_input(input_obj: Any) -> bool:
    """Check if the input object is a tool input."""
    return (
        isinstance(input_obj, dict)
        and 'selected_agent' in input_obj
        and 'confidence' in input_obj
    )

def conversation_to_dict(
    conversation:
        ConversationMessage |
        TimestampedMessage |
        list[ConversationMessage | TimestampedMessage]
) -> dict[str, Any] | list[dict[str, Any]]:
    """Convert conversation to dictionary format."""
    if isinstance(conversation, list):
        return [message_to_dict(msg) for msg in conversation]
    return message_to_dict(conversation)

def message_to_dict(message: ConversationMessage | TimestampedMessage) -> dict[str, Any]:
    """Convert a single message to dictionary format."""
    # result = {
    #     "role": message.role.value if hasattr(message.role, 'value') else str(message.role),
    #     "content": message.content
    # }
    # if isinstance(message, TimestampedMessage):
    #     result["timestamp"] = message.timestamp
    # return result

    # Filter out empty content blocks
    if isinstance(message.content, list):
        filtered_content = []
        for block in message.content:
            if isinstance(block, dict):
                # For text blocks, ensure they have non-empty text
                if "text" in block and not block["text"]:
                    continue
                # For toolUse blocks, ensure they have valid input
                if "toolUse" in block and (not block["toolUse"].get("input") or block["toolUse"].get("input") == ""):
                    continue
            filtered_content.append(block)
        content = filtered_content if filtered_content else [{"text": " "}]  # Fallback to avoid empty content
    else:
        content = message.content
    
    result = {
        "role": (
            message.role.value if hasattr(message.role, "value") else str(message.role)
        ),
        "content": content,
    }
    if isinstance(message, TimestampedMessage):
        result["timestamp"] = message.timestamp
    return result
