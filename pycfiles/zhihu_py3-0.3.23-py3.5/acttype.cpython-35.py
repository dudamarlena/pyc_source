# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zhihu/acttype.py
# Compiled at: 2016-02-17 02:27:50
# Size of source mod 2**32: 2557 bytes
import enum
match = {'ANSWER_QUESTION': 'member_answer_question', 
 'UPVOTE_ANSWER': 'member_voteup_answer', 
 'ASK_QUESTION': 'member_ask_question', 
 'FOLLOW_QUESTION': 'member_follow_question', 
 'UPVOTE_POST': 'member_voteup_article', 
 'FOLLOW_COLUMN': 'member_follow_column', 
 'FOLLOW_TOPIC': 'member_follow_topic', 
 'PUBLISH_POST': 'member_create_article', 
 'FOLLOW_COLLECTION': 'member_follow_favlist'}
reverse_match = {v:k for k, v in match.items()}

class ActType(enum.Enum):
    __doc__ = '用于表示用户动态的类型.\n\n    :常量说明:\n        ================= ================ ============ =====================\n        常量名              说明              提供属性      属性类型\n        ================= ================ ============ =====================\n        ANSWER_QUESTION   回答了一个问题    answer       :class:`.Answer`\n        UPVOTE_ANSWER     赞同了一个回答    answer       :class:`.Answer`\n        ASK_QUESTION      提出了一个问题    question     :class:`.Question`\n        FOLLOW_QUESTION   关注了一个问题    question     :class:`.Question`\n        UPVOTE_POST       赞同了一篇文章    post         :class:`.Post`\n        FOLLOW_COLUMN     关注了一个专栏    column       :class:`.Column`\n        FOLLOW_TOPIC      关注了一个话题    topic        :class:`.Topic`\n        PUBLISH_POST      发表了一篇文章    post         :class:`.Post`\n        FOLLOW_COLLECTION 关注了一个收藏夹  collection   :class:`.Collection`\n        ================= ================ ============ =====================\n\n    '
    ANSWER_QUESTION = 1
    UPVOTE_ANSWER = 2
    ASK_QUESTION = 4
    FOLLOW_QUESTION = 8
    UPVOTE_POST = 16
    FOLLOW_COLUMN = 32
    FOLLOW_TOPIC = 64
    PUBLISH_POST = 128
    FOLLOW_COLLECTION = 256

    @classmethod
    def from_str(cls, div_class):
        return cls.__getattr__(reverse_match[div_class])

    def __str__(self):
        return match[self.name]


class CollectActType(enum.Enum):
    __doc__ = '用于表示收藏夹操作的类型.\n\n    :常量说明:\n        ================= ==============\n        常量名            说明\n        ================= ==============\n        INSERT_ANSWER     在收藏夹中增加一个回答\n        DELETE_ANSWER     在收藏夹中删除一个回答\n        CREATE_COLLECTION 创建收藏夹\n        ================= ==============\n    '
    INSERT_ANSWER = 1
    DELETE_ANSWER = 2
    CREATE_COLLECTION = 3