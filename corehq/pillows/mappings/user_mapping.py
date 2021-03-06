from corehq.util.elastic import es_index
from pillowtop.es_utils import ElasticsearchIndexInfo

USER_INDEX = es_index("hqusers_2016-07-19")
USER_MAPPING={'_all': {'analyzer': 'standard'},
 '_meta': {'created': None},
 'date_detection': False,
 'date_formats': ['yyyy-MM-dd',
                  "yyyy-MM-dd'T'HH:mm:ssZZ",
                  "yyyy-MM-dd'T'HH:mm:ss.SSSSSS",
                  "yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'",
                  "yyyy-MM-dd'T'HH:mm:ss'Z'",
                  "yyyy-MM-dd'T'HH:mm:ssZ",
                  "yyyy-MM-dd'T'HH:mm:ssZZ'Z'",
                  "yyyy-MM-dd'T'HH:mm:ss.SSSZZ",
                  "yyyy-MM-dd'T'HH:mm:ss",
                  "yyyy-MM-dd' 'HH:mm:ss",
                  "yyyy-MM-dd' 'HH:mm:ss.SSSSSS",
                  "mm/dd/yy' 'HH:mm:ss"],
 'dynamic': False,
 'properties': {'CURRENT_VERSION': {'type': 'string'},
                'base_doc': {'type': 'string'},
                'created_on': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                               'type': 'date'},
                'date_joined': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                'type': 'date'},
                'doc_type': {'index': 'not_analyzed', 'type': 'string'},
                'domain': {'fields': {'domain': {'index': 'analyzed',
                                                 'type': 'string'},
                                      'exact': {'index': 'not_analyzed',
                                                'type': 'string'}},
                           'type': 'multi_field'},
                'location_id': {'index': 'not_analyzed', 'type': 'string'},
                'domain_membership': {'dynamic': False,
                                      'properties': {'doc_type': {'index': 'not_analyzed',
                                                                  'type': 'string'},
                                                     'domain': {'fields': {'domain': {'index': 'analyzed',
                                                                                      'type': 'string'},
                                                                           'exact': {'index': 'not_analyzed',
                                                                                     'type': 'string'}},
                                                                'type': 'multi_field'},
                                                     'is_admin': {'type': 'boolean'},
                                                     'override_global_tz': {'type': 'boolean'},
                                                     'role_id': {'type': 'string'},
                                                     'timezone': {'type': 'string'},
                                                     'location_id': {'index': 'not_analyzed',
                                                                     'type': 'string'}},
                                      'type': 'object'},
                'domain_memberships': {'dynamic': False,
                                      'properties': {'doc_type': {'index': 'not_analyzed',
                                                                  'type': 'string'},
                                                     'domain': {'fields': {'domain': {'index': 'analyzed',
                                                                                      'type': 'string'},
                                                                           'exact': {'index': 'not_analyzed',
                                                                                     'type': 'string'}},
                                                                'type': 'multi_field'},
                                                     'is_admin': {'type': 'boolean'},
                                                     'override_global_tz': {'type': 'boolean'},
                                                     'role_id': {'type': 'string'},
                                                     'timezone': {'type': 'string'},
                                                     'location_id': {'index': 'not_analyzed',
                                                                     'type': 'string'}},
                                      'type': 'object'},
                'email_opt_out': {'type': 'boolean'},
                'eulas': {'dynamic': False,
                          'properties': {'date': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                                  'type': 'date'},
                                         'doc_type': {'index': 'not_analyzed',
                                                      'type': 'string'},
                                         'signed': {'type': 'boolean'},
                                         'type': {'type': 'string'},
                                         'user_id': {'type': 'string'},
                                         'user_ip': {'type': 'string'},
                                         'version': {'type': 'string'}},
                          'type': 'object'},
                'first_name': {'type': 'string'},
                'is_active': {'type': 'boolean'},
                'is_staff': {'type': 'boolean'},
                'is_superuser': {'type': 'boolean'},
                'language': {'type': 'string'},
                'last_login': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                               'type': 'date'},
                'last_name': {'type': 'string'},
                'password': {'type': 'string'},
                'registering_device_id': {'type': 'string'},
                'status': {'type': 'string'},
                'user_data': {'type': 'object', 'enabled': False},
                'base_username': {'fields': {'base_username': {'index': 'analyzed',
                                                               'type': 'string'},
                                             'exact': {'index': 'not_analyzed',
                                                       'type': 'string'}},
                                 'type': 'multi_field'},
                'username': {'fields': {'exact': {'include_in_all': False,
                                                  'index': 'not_analyzed',
                                                  'type': 'string'},
                                        'username': {'analyzer': 'standard',
                                                     'index': 'analyzed',
                                                     'type': 'string'}},
                             'type': 'multi_field'},
                '__group_ids': {'type': 'string'},
                '__group_names': {'fields': {'__group_names': { 'index': 'analyzed',
                                                                'type': 'string'},
                                             'exact': {'index': 'not_analyzed',
                                                                'type': 'string'}},
                                  'type': 'multi_field'}}}

USER_META = {
    "settings": {
        "analysis": {
            "analyzer": {
                "default": {
                    "type": "custom",
                    "tokenizer": "whitespace",
                    "filter": ["lowercase"]
                },
            }
        }
    }
}


USER_INDEX_INFO = ElasticsearchIndexInfo(
    index=USER_INDEX,
    alias='hqusers',
    type='user',
    meta=USER_META,
    mapping=USER_MAPPING,
)
