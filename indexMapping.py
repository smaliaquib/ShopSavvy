indexMapping = {
    "properties": {
        "product_id":{
            "type": "long"

        },
        "product_image":{
            "type": "text"

        },
        "product_link":{
            "type": "text"

        },
        "product_price":{
            "type": "text"

        },
        "product_title":{
            "type": "text"

        },
        "product_description":{
            "type": "text"

        },
        "category":{
            "type": "text"

        },
        "real_price":{
            "type": "long"
        },
        "name_description_vector":{
            "type": "dense_vector",
            "dims": 1536,
            "index": True,
            "similarity": "cosine"
        }
    }
}
