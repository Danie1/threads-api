from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class FriendshipStatus(BaseModel):
    following: Optional[bool] = None
    followed_by: Optional[bool] = None
    blocking: Optional[bool] = None
    muting: Optional[bool] = None
    is_private: Optional[bool] = None
    incoming_request: Optional[bool] = None
    outgoing_request: Optional[bool] = None
    is_bestie: Optional[bool] = None
    is_restricted: Optional[bool] = None
    is_feed_favorite: Optional[bool] = None
    subscribed: Optional[bool] = None
    is_eligible_to_subscribe: Optional[bool] = None
    text_post_app_pre_following: bool = None

class FriendData(BaseModel):
    friendship_status: Optional[FriendshipStatus] = None
    previous_following: Optional[bool] = None
    status: Optional[str] = None

class HdProfilePicInfo(BaseModel):
    url: str = None
    width: int = None
    height: int = None

class User(BaseModel):
    has_anonymous_profile_picture: bool = None
    follower_count: int = None
    media_count: int = None
    following_count: int = None
    following_tag_count: int = None
    fbid_v2: str = None
    has_onboarded_to_text_post_app: bool = None
    show_text_post_app_badge: bool = None
    text_post_app_joiner_number: int = None
    show_ig_app_switcher_badge: bool = None
    pk: int = None
    pk_id: str = None
    username: str = None
    full_name: str = None
    is_private: bool = None
    is_verified: bool = None
    profile_pic_id: str = None
    profile_pic_url: str = None
    has_opt_eligible_shop: bool = None
    account_badges: List[str] = None
    third_party_downloads_enabled: int = None
    unseen_count: int = None
    friendship_status: FriendshipStatus = None
    latest_reel_media: int = None
    should_show_category: bool = None
    biography: str = None
    biography_with_entities: Dict[str, Any] = None
    can_link_entities_in_bio: bool = None
    external_url: str = None
    primary_profile_link_type: int = None
    show_fb_link_on_profile: bool = None
    show_fb_page_link_on_profile: bool = None
    can_hide_category: bool = None
    category: str = None
    is_category_tappable: bool = None
    is_business: bool = None
    professional_conversion_suggested_account_type: int = None
    account_type: int = None
    displayed_action_button_partner: str = None
    smb_delivery_partner: str = None
    smb_support_delivery_partner: str = None
    displayed_action_button_type: str = None
    smb_support_partner: str = None
    is_call_to_action_enabled: bool = None
    num_of_admined_pages: int = None
    page_id: str = None
    page_name: str = None
    ads_page_id: str = None
    ads_page_name: str = None
    bio_links: List[Dict[str, str]] = None
    can_add_fb_group_link_on_profile: bool = None
    eligible_shopping_signup_entrypoints: List[str] = None
    is_igd_product_picker_enabled: bool = None
    eligible_shopping_formats: List[str] = None
    needs_to_accept_shopping_seller_onboarding_terms: bool = None
    is_shopping_settings_enabled: bool = None
    is_shopping_community_content_enabled: bool = None
    is_shopping_auto_highlight_eligible: bool = None
    is_shopping_catalog_source_selection_enabled: bool = None
    current_catalog_id: str = None
    mini_shop_seller_onboarding_status: str = None
    shopping_post_onboard_nux_type: str = None
    ads_incentive_expiration_date: str = None
    can_be_tagged_as_sponsor: bool = None
    can_boost_post: bool = None
    can_convert_to_business: bool = None
    can_create_new_standalone_fundraiser: bool = None
    can_create_new_standalone_personal_fundraisers: bool = None
    can_create_sponsor_tags: bool = None
    can_see_organic_insights: bool = None
    has_chaining: bool = None
    has_guides: bool = None
    has_placed_orders: bool = None
    hd_profile_pic_url_info: HdProfilePicInfo = None
    hd_profile_pic_versions: List[HdProfilePicInfo] = None
    is_allowed_to_create_standalone_nonprofit_fundraisers: bool = None
    is_allowed_to_create_standalone_personal_fundraisers: bool = None
    pinned_channels_info: Dict[str, Any] = None
    show_conversion_edit_entry: bool = None
    show_insights_terms: bool = None
    show_text_post_app_switcher_badge: bool = None
    total_clips_count: int = None
    total_igtv_videos: int = None
    usertags_count: int = None
    usertag_review_enabled: bool = None
    fan_club_info: Optional[dict] = None
    transparency_product_enabled: Optional[bool] = None
    text_post_app_take_a_break_setting: Optional[int] = None
    interop_messaging_user_fbid: Optional[int] = None
    allowed_commenter_type: Optional[str] = None
    is_unpublished: Optional[bool] = None
    reel_auto_archive: Optional[str] = None
    feed_post_reshare_disabled: Optional[bool] = None
    show_account_transparency_details: Optional[bool] = None

class UsersList(BaseModel):
    users: List[User] = None

class ImageVersion(BaseModel):
    url: str = None

class CarouselMedia(BaseModel):
    image_versions2: Dict[str, List[ImageVersion]] = None

class VideoVersion(BaseModel):
    type: Optional[int] = None
    url: Optional[str] = None
    _typename: Optional[str] = Field(None, alias="__typename")

class Caption(BaseModel):
    pk: Optional[str] = None
    user_id: Optional[int] = None
    text: Optional[str] = None
    type: Optional[int] = None
    created_at: Optional[int] = None
    created_at_utc: Optional[int] = None
    content_type: Optional[str] = None
    status: Optional[str] = None
    bit_flags: Optional[int] = None
    did_report_as_spam: Optional[bool] = None
    share_enabled: Optional[bool] = None
    user: Optional[User] = None
    is_covered: Optional[bool] = None
    is_ranked_comment: Optional[bool] = None
    media_id: Optional[int] = None
    private_reply_status: Optional[int] = None

class ShareInfo(BaseModel):
    can_repost: Optional[bool] = None
    is_reposted_by_viewer: Optional[bool] = None
    repost_restricted_reason: Optional[str] = None
    can_quote_post: Optional[bool] = None
    quoted_post: Optional[dict] = None
    reposted_post: Optional[dict] = None

class TextPostAppInfo(BaseModel):
    is_post_unavailable: Optional[bool] = None
    is_reply: Optional[bool] = None
    reply_to_author: Optional[User] = None
    direct_reply_count: Optional[int] = None
    self_thread_count: Optional[int] = None
    reply_facepile_users: List[dict] = None
    link_preview_attachment: Optional[dict] = None
    can_reply: Optional[bool] = None
    reply_control: Optional[str] = None
    hush_info: Optional[dict] = None
    share_info: Optional[ShareInfo] = None

class VideoVersions(BaseModel):
    type: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    url: Optional[str] = None
    id: Optional[str] = None

class ImageCandidate(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None
    url: Optional[str] = None
    scans_profile: Optional[str] = None

class ImageVersions2(BaseModel):
    candidates: Optional[List[ImageCandidate]] = None

class Post(BaseModel):
    pk: Optional[int] = None
    id: Optional[str] = None
    taken_at: Optional[int] = None
    device_timestamp: Optional[int] = None
    client_cache_key: Optional[str] = None
    filter_type: Optional[int] = None
    like_and_view_counts_disabled: Optional[bool] = None
    integrity_review_decision: Optional[str] = None
    text_post_app_info: Optional[TextPostAppInfo] = None
    caption: Optional[Caption] = None
    media_type: Optional[int] = None
    code: Optional[str] = None
    carousel_media: List[CarouselMedia] = None
    carousel_media_count: int = None
    product_type: Optional[str] = None
    organic_tracking_token: Optional[str] = None
    image_versions2: Optional[ImageVersions2] = None
    original_width: Optional[int] = None
    original_height: Optional[int] = None
    is_dash_eligible: Optional[int] = None
    is_dash: Optional[bool] = None
    video_dash_manifest: Optional[str] = None
    video_codec: Optional[str] = None
    has_audio: Optional[bool] = None
    video_duration: Optional[float] = None
    video_versions: List[VideoVersions] = None
    like_count: Optional[int] = None
    has_liked: Optional[bool] = None
    can_viewer_reshare: Optional[bool] = None
    top_likers: List[dict] = []
    user: Optional[User] = None
    media_overlay_info: Dict[str, Any] = None
    logging_info_token: Optional[str] = None

class ThreadItem(BaseModel):
    post: Post = None
    line_type: str = None
    view_replies_cta_string: str = None
    reply_facepile_users: List[Dict[str, Any]] = None
    should_show_replies_cta: bool = None
    reply_to_author: Optional[User] = None
    can_inline_expand_below: bool = None
    _typename: Optional[str] = Field(None, alias="__typename")

class Thread(BaseModel):
    thread_items: List[ThreadItem] = None
    id: str = None
    thread_type: str = None
    header: Optional[dict] = None

class Threads(BaseModel):
    threads: List[Thread] = None

class Replies(BaseModel):
    containing_thread: Optional[Thread] = None
    reply_threads: Optional[List[Thread]] = None

class FundraiserTag(BaseModel):
    has_standalone_fundraiser: Optional[bool] = None


class MusicMetadata(BaseModel):
    music_canonical_id: Optional[str] = None
    audio_type: Optional[str] = None
    music_info: Optional[dict] = None
    original_sound_info: Optional[dict] = None
    pinned_media_ids: Optional[dict] = None

class SharingFrictionInfo(BaseModel):
    should_have_sharing_friction: Optional[bool] = None
    bloks_app_url: Optional[str] = None
    sharing_friction_payload: Optional[str] = None

class MashupInfo(BaseModel):
    mashups_allowed: Optional[bool] = None
    can_toggle_mashups_allowed: Optional[bool] = None
    has_been_mashed_up: Optional[bool] = None
    is_light_weight_check: Optional[bool] = None
    formatted_mashups_count: Optional[int] = None
    original_media: Optional[dict] = None
    privacy_filtered_mashups_media_count: Optional[int] = None
    non_privacy_filtered_mashups_media_count: Optional[int] = None
    mashup_type: Optional[str] = None
    is_creator_requesting_mashup: Optional[bool] = None
    has_nonmimicable_additional_audio: Optional[bool] = None
    is_pivot_page_available: Optional[bool] = None

class MediaData(BaseModel):
    taken_at: Optional[int] = None
    pk: Optional[int] = None
    id: Optional[str] = None
    device_timestamp: Optional[int] = None
    client_cache_key: Optional[str] = None
    filter_type: Optional[int] = None
    fundraiser_tag: Optional[FundraiserTag] = None
    caption_is_edited: Optional[bool] = None
    like_and_view_counts_disabled: Optional[bool] = None
    is_in_profile_grid: Optional[bool] = None
    is_reshare_of_text_post_app_media_in_ig: Optional[bool] = None
    media_type: Optional[int] = None
    code: Optional[str] = None
    can_viewer_reshare: Optional[bool] = None
    caption: Optional[Caption] = None
    clips_tab_pinned_user_ids: Optional[List[dict]] = None
    comment_inform_treatment: Optional[dict] = None
    sharing_friction_info: Optional[SharingFrictionInfo] = None
    xpost_deny_reason: Optional[str] = None
    original_media_has_visual_reply_media: Optional[bool] = None
    fb_user_tags: Optional[dict] = None
    mashup_info: Optional[MashupInfo] = None
    can_viewer_save: Optional[bool] = None
    profile_grid_control_enabled: Optional[bool] = None
    featured_products: Optional[List[dict]] = None
    is_comments_gif_composer_enabled: Optional[bool] = None
    product_suggestions: Optional[List[dict]] = None
    user: Optional[User] = None
    image_versions2: Optional[dict] = None
    original_width: Optional[int] = None
    original_height: Optional[int] = None
    max_num_visible_preview_comments: Optional[int] = None
    has_more_comments: Optional[bool] = None
    comment_threading_enabled: Optional[bool] = None
    preview_comments: Optional[List[dict]] = None
    comment_count: Optional[int] = None
    can_view_more_preview_comments: Optional[bool] = None
    hide_view_all_comment_entrypoint: Optional[bool] = None
    likers: Optional[List[dict]] = None
    shop_routing_user_id: Optional[str] = None
    can_see_insights_as_brand: Optional[bool] = None
    is_organic_product_tagging_eligible: Optional[bool] = None
    music_metadata: Optional[MusicMetadata] = None
    deleted_reason: Optional[int] = None
    integrity_review_decision: Optional[str] = None
    has_shared_to_fb: Optional[int] = None
    is_unified_video: Optional[bool] = None
    should_request_ads: Optional[bool] = None
    is_visual_reply_commenter_notice_enabled: Optional[bool] = None
    commerciality_status: Optional[str] = None
    explore_hide_comments: Optional[bool] = None
    product_type: Optional[str] = None
    is_paid_partnership: Optional[bool] = None
    organic_tracking_token: Optional[str] = None
    text_post_app_info: Optional[dict] = None
    ig_media_sharing_disabled: Optional[bool] = None
    has_delayed_metadata: Optional[bool] = None

class PostResponse(BaseModel):
    media: Optional[MediaData] = None
    upload_id: Optional[str] = None
    status: Optional[str] = None

class CarouselMedia(BaseModel):
    media_type: Optional[int] = None
    image_versions2: Optional[ImageVersions2] = None
    original_width: Optional[int] = None
    original_height: Optional[int] = None
    pk: Optional[int] = None

class Comment(BaseModel):
    pk: Optional[int] = None
    user_id: Optional[int] = None
    text: Optional[str] = None
    created_at: Optional[int] = None
    content_type: Optional[str] = None
    status: Optional[str] = None
    share_enabled: Optional[bool] = None
    has_translation: Optional[bool] = None
    parent_comment_id: Optional[int] = None
    media_info: Optional[Post] = None
    user: Optional[User] = None

class TimelineItem(BaseModel):
    thread_items: Optional[List[ThreadItem]] = None
    header: Optional[dict] = None
    thread_type: Optional[str] = None
    show_create_reply_cta: Optional[bool] = None
    id: Optional[int] = None
    view_state_item_type: Optional[int] = None
    posts: List[Post] = []

class TimelineData(BaseModel):
    num_results: Optional[int] = None
    more_available: Optional[bool] = None
    auto_load_more_enabled: Optional[bool] = None
    is_direct_v2_enabled: Optional[bool] = None
    next_max_id: Optional[str] = None
    view_state_version: Optional[str] = None
    client_feed_changelist_applied: Optional[bool] = None
    request_id: Optional[str] = None
    pull_to_refresh_window_ms: Optional[int] = None
    preload_distance: Optional[int] = None
    status: Optional[str] = None
    pagination_source: Optional[str] = None
    hide_like_and_view_counts: Optional[int] = None
    last_head_load_ms: Optional[int] = None
    is_shell_response: Optional[bool] = None
    feed_items_media_info : Optional[List[dict]] = None
    items: List[TimelineItem] = []
