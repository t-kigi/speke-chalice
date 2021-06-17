{
  "version": "2.0",
  "app_name": "speke-server",
  "environment_variables": {
    "S3BUCKET": "<INPUT YOUR BUCKET NAME>",
    "KEY_PUBLISH_WEBSITE": "<INPUT YOUR WEBSITE which provides the KEY file such as https://example.com>,
    "KEY_PUBLISH_PREFIX": "<INPUT YOUR S3 and WEBSITE prefix such as keys>",
    "SYSTEM_ID": "<INPUT YOUR KEY SERVER SYSTEM ID if needed>"
  },
  "stages": {
    "dev": {
      "api_gateway_stage": "speke-server-dev",
      "autogen_policy": false,
      "lambda_timeout": 10,
      "lambda_memory_size": 512
    },
    "local": {
      "environment_variables": {
        "PROFILE": "work",
        "STAGE": "local"
      }
    }
  }
}
