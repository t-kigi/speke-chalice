# SPEKE Chalice

**This project re-used [SPEKE reference server](https://github.com/awslabs/speke-reference-server) project so all contents extend source license.**

Implementation SPEKE interface only HES AES format by chalice.


# Objective

- extract only HLS AES API implementation part
- parent project uses zappa but I want to use Chalice
- stop to use SecretsManager due to cost reason
  - of course it is more secure to use SecretsManager but to use S3 bucekt only is more cheap


# Setup

## for development

```bash
$ cd [project directory]
$ pipenv install
```


## config.json

Set your parameters (environment_variables) into `src/.chalice/config.json` .

```bash
# copy config file from template
$ cp src/.chalice/config.json.tpl src/.chalice/config.json

# edit it
$ vim src/.chalice/config.json
```

Each content means;

- `S3BUCKET` : The name of bucket which stores encrypt key file
- `KEY_PUBLISH_WEBSITE` : The website url which provides key file such as https://example.com (no ends with `/`)
- `KEY_PUBLISH_PREFIX` : The prefix string both s3 key and website url 
- `SYSTEM_ID` : The UUID if needed. "81376844-f976-481e-a84e-cc25d39b0b33" is used when no input


For example, I set following;

```
"environment_variables": {
  "S3BUCKET": "example-bucket",
  "KEY_PUBLISH_WEBSITE": "https://example.com",
  "KEY_PUBLISH_PREFIX": "keys",
  "SYSTEM_ID": "18f55148-668f-447a-b4f5-298869e84cf1"
},
```

Then, 

- Key files are stored on `s3://example-bucket/keys/[Resource Id]/[kid]`
- Key files are able to download from `https://example.com/keys/[Resource Id]/[kid]`
  - `https://example.com/keys/[Resource Id]/[kid]` is written on hls playlist file (`.m3u8`)

Note that `[Resource Id]` set Media Services parameter, and, `[kid]` is generated automatically by Media Services.


## policy-dev.json

Set your IAM policy into `src/.chalice/policy-dev.json` .

```bash
# copy policy file from template
$ cp src/.chalice/policy-dev.json.tpl src/.chalice/policy.json

# edit it
$ vim src/.chalice/policy.json
```

You input `BUCKET NAME` into `policy.json` .


# Deploy

```bash
$ pipenv run chalice deploy --stage dev [--profile your-profile-if-needed]
```

Or, you can make new stage like `prod` and deploy it. 
Moreover you can deploy by cloudformation by results of `chalice package` command.


# License

Apache License 2.0
