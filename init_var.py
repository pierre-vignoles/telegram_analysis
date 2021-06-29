def init_var_function():
    # Dict of the label/value of the different medias
    dict_media = {"all_media": "All the medias",
                  "text": "Text messages",
                  "media_type_photo": "Photos",
                  "media_type_video_file": "Videos",
                  "media_type_sticker": "Stickers",
                  "media_type_voice_message": "Voice messages",
                  "media_type_phone_call": "Phone call",
                  "media_type_audio_file": "Audio files",
                  "media_type_animation": "Animations",
                  "media_type_emoji": "Emoji",
                  "media_type_link": "Links"}
    dict_media_singular = {"all_media": "media",
                           "text": "text message",
                           "media_type_photo": "photo",
                           "media_type_video_file": "video",
                           "media_type_sticker": "sticker",
                           "Voice media_type_voice_message": "voice message",
                           "media_type_phone_call": "phone call",
                           "media_type_audio_file": "audio file",
                           "media_type_animation": "animation",
                           "media_type_emoji": "emoji",
                           "media_type_link": "link"}

    return dict_media, dict_media_singular
