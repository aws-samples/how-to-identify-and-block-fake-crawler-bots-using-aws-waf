## How to identify and block fake crawler bots using AWS WAF

This repository contains supporting files for the blog post on 'How to identify and block fake crawler bots using AWS WAF'. We will be focusing on how to identify fake bots using these AWS services: AWS WAF (WAF or WebACL), Amazon Kinesis Data Firehose (Firehose), Amazon S3 (S3) and AWS Lambda (Lambda). We are using fake Google/Bing bots to demonstrate, but the principles can be applied to other popular crawlers like Slurp Bot from Yahoo, DuckDuckBot from DuckDuckGo, Alexa crawler from Alexa internet ranking service, etc.

For industries like media, online retailers, news, or social websites, content is critical and often sets them apart from other competitors. These companies put in a significant amount of effort to make the content as visible and accessible as possible. To do that these companies rely on crawler bots so that legitimate users searching for content can find the content easily. Crawler bots are useful for indexing the site pages and helping make the content more searchable and improve rankings. 

However, this capability can be misused. So it is important to distinguish between genuine crawler bots and fake ones that are doing more than just indexing your site. It’s important to properly identify good and bad actors so that you can stop the bad ones without impacting the ability of good ones, and at scale. This helps in driving more traffic, visitors, and more revenue from your websites.


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

