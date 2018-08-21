from pony.orm import *

from cosmoquest_data_tools.config import config

from datetime import datetime


db = Database()


class Application(db.Entity):
    _table_ = "applications"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    name = Optional(str, 255, unique=True)
    title = Optional(str, 255)
    active = Optional(bool, default=True)
    description = Optional(LongStr)
    type = Optional(str, 255, default="standard")
    background_url = Optional(str, 255)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    scistarter_project_id = Optional(str, 255)
    project = Optional("Project", column="project_id")
    images = Set("Image")
    image_sets = Set("ImageSet")
    marks = Set("Mark")
    shared_marks = Set("SharedMark")
    verified_marks = Set("VerifiedMark")
    image_users = Set("ImageUser")
    role_users = Set("RoleUser")


class Badge(db.Entity):
    _table_ = "badges"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    name = Optional(str, 255, unique=True)
    description = Optional(LongStr)
    excerpt = Optional(LongStr)
    image_location = Optional(LongStr)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    giveaway_size = Optional(int, size=16)
    unlock_codes = Set("UnlockCode")
    badge_users = Set("BadgeUser")
    giveaway_winners = Set("GiveawayWinner")


class BadgeUser(db.Entity):
    _table_ = "badge_users"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    badge = Required("Badge", column="badge_id")
    user = Required("User", column="user_id")
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")


class DetectiveData(db.Entity):
    _table_ = "detective_datas"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    image = Required("Image", column="image_id")
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    center_lat = Optional(float)
    center_lng = Optional(float)
    top_left_lat = Optional(float)
    top_left_lng = Optional(float)
    top_right_lat = Optional(float)
    top_right_lng = Optional(float)
    bottom_left_lat = Optional(float)
    bottom_left_lng = Optional(float)
    bottom_right_lat = Optional(float)
    bottom_right_lng = Optional(float)
    rotation = Optional(float)
    off_nadir = Optional(float)
    standard_distance = Optional(float)
    required_precision = Optional(float)
    cloud_bin = Optional(int, size=8)
    tag_bins = Optional(LongStr)
    user_tag_ids = Optional(LongStr)
    in_range_image_user_ids = Optional(LongStr)
    out_range_image_user_ids = Optional(LongStr)
    image_user_ids = Optional(LongStr)
    validated = Optional(bool)


class GiveawayWinner(db.Entity):
    _table_ = "giveaway_winners"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    user = Required("User", column="user_id")
    badge = Required(Badge, column="badge_id")


class Image(db.Entity):
    _table_ = "images"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    image_set = Optional("ImageSet", column="image_set_id")
    name = Optional(str, 255, unique=True)
    file_location = Optional(LongStr)
    priority = Optional(float)
    premarked = Optional(bool, default=False)
    done = Optional(bool, default=False)
    sun_angle = Optional(float)
    details = Optional(LongStr)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    favorites_count = Optional(int, size=16, default=0, unsigned=True)
    application = Optional("Application", column="application_id")
    detective_datas = Set("DetectiveData")
    marks = Set("Mark")
    shared_marks = Set("SharedMark")
    verified_marks = Set("VerifiedMark")
    image_users = Set("ImageUser")


class ImageSet(db.Entity):
    _table_ = "image_sets"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    name = Optional(str, 255, unique=True)
    application = Required("Application", column="application_id")
    images = Set(Image)
    priority = Optional(float)
    sun_angle = Optional(float)
    minimum_latitude = Optional(float)
    maximum_latitude = Optional(float)
    minimum_longitude = Optional(float)
    maximum_longitude = Optional(float)
    pixel_resolution = Optional(float)
    description = Optional(LongStr)
    details = Optional(LongStr)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")


class ImageUser(db.Entity):
    _table_ = "image_users"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    user = Required("User", column="user_id")
    image = Required("Image", column="image_id")
    application = Required("Application", column="application_id")
    submit_time = Optional(int, size=16, unsigned=True)
    score = Optional(int, size=16, unsigned=True)
    premarked = Optional(bool, default=False)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    details = Optional(LongStr)
    validated_center = Optional(bool)
    image_user_tags = Set("ImageUserTag")


class ImageUserTag(db.Entity):
    _table_ = "image_user_tags"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    tag = Required("Tag", column="tag_id")
    image_user = Required("ImageUser", column="image_user_id")
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    validated_bin = Optional(bool)


class Mark(db.Entity):
    _table_ = "marks"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    application = Required("Application", column="application_id")
    image = Required("Image", column="image_id")
    image_user_id = Optional(int, size=16, unsigned=True)
    machine_mark_id = Optional(int, size=16, unsigned=True)
    shared_mark_id = Optional(int, size=16, unsigned=True)
    x = Optional(float)
    y = Optional(float)
    diameter = Optional(float)
    submit_time = Optional(int, size=16, unsigned=True)
    confirmed = Optional(bool)
    score = Optional(float)
    type = Optional(str, 255)
    sub_type = Optional(str, 255, nullable=True)
    details = Optional(LongStr)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    user = Required("User", column="user_id")


class Project(db.Entity):
    _table_ = "projects"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    name = Optional(str, 255)
    title = Optional(LongStr)
    description = Optional(LongStr)
    type = Optional(str, 255)
    applications = Set("Application")
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    storage_server_url = Optional(str, 255)
    storage_server_port = Optional(int, size=16)
    storage_server_password = Optional(str, 255)
    storage_server_is_sftp = Optional(bool)
    admin_id = Optional(int, size=16, unsigned=True)
    storage_server_is_passive = Optional(bool)


class Role(db.Entity):
    _table_ = "roles"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    name = Optional(str, 255, unique=True)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    role_users = Set("RoleUser")


class RoleUser(db.Entity):
    _table_ = "role_users"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    role = Required("Role", column="role_id")
    user = Required("User", column="user_id")
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    application = Optional("Application", column="application_id")


class SharedMark(db.Entity):
    _table_ = "shared_marks"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    image = Required("Image", column="image_id")
    x = Optional(float)
    y = Optional(float)
    diameter = Optional(float)
    confidence = Optional(float)
    type = Optional(str, 255)
    sub_type = Optional(str, 255, nullable=True)
    details = Optional(LongStr)
    verified = Optional(bool, default=False)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    application = Required("Application", column="application_id")
    verified_marks = Set("VerifiedMark")


class SocialMediaProvider(db.Entity):
    _table_ = "social_media_providers"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    provider = Optional(str, 255)
    token = Optional(str, 255, unique=True)
    provider_id = Optional(str, 255)
    provider_url = Optional(str, 255, nullable=True)
    user = Required("User", column="user_id")


class Tag(db.Entity):
    _table_ = "tags"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    name = Optional(str, 255, unique=True)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    image_user_tags = Set("ImageUserTag")


class Team(db.Entity):
    _table_ = "teams"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    name = Optional(str, 255, unique=True)
    type = Optional(str, 255)
    join_code = Optional(str, 255)
    description = Optional(LongStr)
    admin_id = Optional(int, size=16, unsigned=True)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    team_users = Set("TeamUser")


class TeamUser(db.Entity):
    _table_ = "team_users"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    team = Required("Team", column="team_id")
    user = Required("User", column="user_id")
    status = Optional(str, 255)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")


class UnlockCode(db.Entity):
    _table_ = "unlock_codes"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    code = Optional(str, 255)
    expiration_date = Optional(datetime, sql_type="DATETIME")
    badge = Required("Badge", column="badge_id")
    unlock_code_users = Set("UnlockCodeUser")


class UnlockCodeUser(db.Entity):
    _table_ = "unlock_code_user"

    id = PrimaryKey(int, size=16, auto=True)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    unlock_code = Required("UnlockCode", column="unlock_code_id")
    user = Required("User", column="user_id")


class User(db.Entity):
    _table_ = "users"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    forum_id = Optional(int, size=16, unsigned=True)
    name = Optional(str, 255, unique=True)
    email = Optional(str, 255, nullable=True)
    password = Optional(str, 255, nullable=True)
    details = Optional(LongStr)
    finished_tutorial = Optional(bool, default=False)
    type = Optional(str, 255, default="standard")
    remember_token = Optional(str, 100, nullable=True)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")
    classroom_user_id = Optional(int, size=16, unsigned=True)
    reset_password = Optional(bool)
    public_profile = Optional(bool, default=True)
    wp_id = Optional(int, size=16, unsigned=True)
    gravatar_url = Optional(str, 255)
    first_name = Optional(str, 255, nullable=True)
    last_name = Optional(str, 255, nullable=True)
    level = Optional(int, size=16, default=0, unsigned=True)
    tutorials_completed = Optional(str, 255)
    scistarter_token = Optional(str, 255, nullable=True)
    scistarter_id = Optional(int, size=16)
    scistarter_profile_url = Optional(str, 255, nullable=True)
    facebook_token = Optional(str, 255, nullable=True)
    twitter_token = Optional(str, 255, nullable=True)
    verified_marks = Set("VerifiedMark")
    badge_users = Set("BadgeUser")
    giveaway_winners = Set("GiveawayWinner")
    image_users = Set("ImageUser")
    marks = Set("Mark")
    role_users = Set("RoleUser")
    social_media_providers = Set("SocialMediaProvider")
    team_users = Set("TeamUser")
    unlock_code_users = Set("UnlockCodeUser")


class VerifiedMark(db.Entity):
    _table_ = "verified_marks"

    id = PrimaryKey(int, size=16, auto=True, unsigned=True)
    user = Required("User", column="user_id")
    image = Required("Image", column="image_id")
    application = Required("Application", column="application_id")
    shared_mark = Optional("SharedMark", column="shared_mark_id")
    x = Optional(float)
    y = Optional(float)
    diameter = Optional(float)
    created_at = Optional(datetime, sql_type="TIMESTAMP")
    updated_at = Optional(datetime, sql_type="TIMESTAMP")


db.bind(
    provider="mysql", 
    host=config["databases"]["cosmoquest-php"]["host"], 
    user=config["databases"]["cosmoquest-php"]["user"], 
    passwd=config["databases"]["cosmoquest-php"]["password"], 
    db=config["databases"]["cosmoquest-php"]["database"]
)

db.generate_mapping(create_tables=False)
