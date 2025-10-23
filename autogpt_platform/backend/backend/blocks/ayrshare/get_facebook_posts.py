from backend.integrations.ayrshare import HistoryPost, HistoryResponse, SocialPlatform
from backend.sdk import (
    Block,
    BlockCategory,
    BlockOutput,
    BlockSchema,
    BlockType,
    SchemaField,
)

from ._util import create_ayrshare_client, get_profile_key


class GetFacebookPostsBlock(Block):
    """Block for retrieving Facebook post history using Ayrshare."""

    class Input(BlockSchema):
        """Input schema for Facebook post retrieval."""

        last_days: int = SchemaField(
            description="Number of days to go back (1-730)",
            default=30,
            advanced=False,
        )
        last_records: int = SchemaField(
            description="Number of records to return (1-100)",
            default=50,
            advanced=True,
        )
        last_key: str = SchemaField(
            description="Pagination key for retrieving next set of results",
            default="",
            advanced=True,
        )

    class Output(BlockSchema):
        # Common outputs
        posts: list[HistoryPost] = SchemaField(
            description="List of Facebook posts from history"
        )
        post: HistoryPost = SchemaField(
            description="Individual post (yielded for each post)"
        )
        next_pagination_key: str = SchemaField(
            description="Key for pagination to get next results"
        )
        error: str = SchemaField(description="Error message if the request failed")

    def __init__(self):
        super().__init__(
            id="e5f6g7h8-5678-4567-89ab-facebookget001",
            description="Retrieve Facebook post history using Ayrshare",
            categories={BlockCategory.SOCIAL},
            block_type=BlockType.AYRSHARE,
            input_schema=GetFacebookPostsBlock.Input,
            output_schema=GetFacebookPostsBlock.Output,
            test_input={
                "last_days": 7,
                "last_records": 10,
                "last_key": "",
            },
            test_output=[
                (
                    "posts",
                    [
                        HistoryPost(
                            id="post456",
                            post="Test Facebook post",
                            platforms=["facebook"],
                            created="2024-01-15T10:30:00Z",
                            status="success",
                        )
                    ],
                ),
                ("next_pagination_key", ""),
            ],
            test_mock={
                "get_facebook_history": lambda *args, **kwargs: HistoryResponse(
                    posts=[
                        HistoryPost(
                            id="post456",
                            post="Test Facebook post",
                            platforms=["facebook"],
                            created="2024-01-15T10:30:00Z",
                            status="success",
                        )
                    ],
                    lastKey=None,
                    lastKeyNext=None,
                )
            },
        )

    @staticmethod
    async def get_facebook_history(
        last_days: int,
        last_records: int,
        last_key: str,
        profile_key: str,
    ) -> HistoryResponse:
        """Retrieve Facebook post history."""
        client = create_ayrshare_client()
        if not client:
            raise ValueError(
                "Ayrshare integration is not configured. Please set up the AYRSHARE_API_KEY."
            )

        response = await client.get_history(
            platforms=[SocialPlatform.FACEBOOK],
            last_days=last_days,
            last_records=last_records,
            last_key=last_key if last_key else None,
            profile_key=profile_key,
        )
        return response

    async def run(
        self,
        input_data: "GetFacebookPostsBlock.Input",
        *,
        user_id: str,
        **kwargs,
    ) -> BlockOutput:
        """Retrieve Facebook posts with Facebook-specific filtering."""
        try:
            profile_key = await get_profile_key(user_id)
            if not profile_key:
                yield "error", "Please link a social account via Ayrshare"
                return

            # Validate input
            if input_data.last_days < 1 or input_data.last_days > 730:
                yield "error", "last_days must be between 1 and 730"
                return

            if input_data.last_records < 1 or input_data.last_records > 100:
                yield "error", "last_records must be between 1 and 100"
                return

            history_response = await self.get_facebook_history(
                last_days=input_data.last_days,
                last_records=input_data.last_records,
                last_key=input_data.last_key,
                profile_key=profile_key.get_secret_value(),
            )

            # Yield all posts as a list
            yield "posts", history_response.posts

            # Yield each post individually
            for post in history_response.posts:
                yield "post", post

            # Yield pagination key for next batch
            next_key = history_response.lastKeyNext or ""
            yield "next_pagination_key", next_key

        except Exception as e:
            yield "error", f"Failed to retrieve Facebook posts: {str(e)}"
