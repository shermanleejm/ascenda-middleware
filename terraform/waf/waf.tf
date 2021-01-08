terraform {
  required_providers {
    aws = {
      version = "~> 2.0"
      null    = "~> 2.0"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = "ap-southeast-1"
}

resource "aws_guardduty_detector" "MyDetector" {
  enable = true
}
resource aws_wafv2_web_acl "itsawaf" {
  name  = "test"
  scope = "REGIONAL"

  default_action {
    allow {}
  }


  rule {
    name     = "AWS-AWSManagedRulesAmazonIpReputationList"
    priority = 0

    override_action {
      count {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesAmazonIpReputationList"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWS-AWSManagedRulesAmazonIpReputationList"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWS-AWSManagedRulesLinuxRuleSet"
    priority = 1

    override_action {
      count {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesLinuxRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWS-AWSManagedRulesLinuxRuleSet"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWS-AWSManagedRulesSQLiRuleSet"
    priority = 2


    override_action {
      count {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesSQLiRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWS-AWSManagedRulesSQLiRuleSet"
      sampled_requests_enabled   = true
    }
  }
  rule {
    name     = "AWS-AWSManagedRulesCommonRuleSet"
    priority = 3

    override_action {
      count {}
    }


    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWS-AWSManagedRulesCommonRuleSet"
      sampled_requests_enabled   = true
    }
  }
  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "test"
    sampled_requests_enabled   = true
  }
}

resource "aws_wafv2_web_acl_association" "web_acl_api_gateway" {
  resource_arn = "arn:aws:apigateway:ap-southeast-1::/restapis/2njpo4jo9a/stages/PROD"
  web_acl_arn  = aws_wafv2_web_acl.itsawaf.arn
}

