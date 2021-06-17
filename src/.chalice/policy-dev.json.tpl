{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
          "s3:*"
      ],
      "Resource": [
          "arn:aws:s3:::<YOUR BUCKET>",
          "arn:aws:s3:::<YOUR BUCKET>/*"
      ],
      "Sid": "S3Access"
    },
    {
        "Effect": "Allow",
        "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*",
        "Sid": "CloudWatchLogsAccess"
    }
  ]
}
