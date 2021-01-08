provider "aws" {
  profile = "default"
  region  = var.region
}

module "vpc" {
  source     = "git::https://github.com/cloudposse/terraform-aws-vpc.git?ref=tags/0.17.0"
  namespace  = var.namespace
  stage      = var.stage
  name       = var.name
  attributes = var.attributes
  tags       = var.tags
  delimiter  = var.delimiter
  cidr_block = "172.16.0.0/16"
}

module "subnets" {
  source               = "git::https://github.com/cloudposse/terraform-aws-dynamic-subnets.git?ref=tags/0.30.0"
  availability_zones   = var.availability_zones
  namespace            = var.namespace
  stage                = var.stage
  name                 = var.name
  attributes           = var.attributes
  tags                 = var.tags
  delimiter            = var.delimiter
  vpc_id               = module.vpc.vpc_id
  igw_id               = module.vpc.igw_id
  cidr_block           = module.vpc.vpc_cidr_block
  nat_gateway_enabled  = true
  nat_instance_enabled = false
}

module "db_sg" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "db-sg"
  description = "Security group for web-server with HTTP ports open within VPC"
  vpc_id      = module.vpc.vpc_id


  ingress_with_source_security_group_id = [
    {
      rule                     = "mysql-tcp"
      source_security_group_id = module.elastic_beanstalk_environment.security_group_id
    }
  ]
  egress_with_source_security_group_id = [
    {
      rule                     = "mysql-tcp"
      source_security_group_id = module.elastic_beanstalk_environment.security_group_id
    }
  ]
}

module "elastic_beanstalk_application" {
  source      = "git::https://github.com/cloudposse/terraform-aws-elastic-beanstalk-application.git?ref=tags/0.7.1"
  namespace   = var.namespace
  stage       = var.stage
  name        = var.name
  attributes  = var.attributes
  tags        = var.tags
  delimiter   = var.delimiter
  description = "Test elastic_beanstalk_application"
}

module "db" {
  source = "terraform-aws-modules/rds/aws"

  identifier = "test-inclass-db"

  # All available versions: http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html#MySQL.Concepts.VersionMgmt
  engine            = "mysql"
  engine_version    = "5.7.19"
  instance_class    = "db.t2.micro"
  allocated_storage = 10
  storage_encrypted = false

  # kms_key_id        = "arm:aws:kms:<region>:<account id>:key/<kms key id>"
  name     = "itsa"
  username = "admin"
  password = "itsabackend"
  port     = "3306"

  vpc_security_group_ids = [module.db_sg.this_security_group_id]

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"

  multi_az = true

  # disable backups to create DB faster
  backup_retention_period = 0

  tags = {
    Owner       = "user"
    Environment = "dev"
  }



  # DB subnet group
  subnet_ids = module.subnets.private_subnet_ids

  # DB parameter group
  family = "mysql5.7"

  # DB option group
  major_engine_version = "5.7"

  # Snapshot name upon DB deletion
  final_snapshot_identifier = "itsa"

  # Database Deletion Protection
  deletion_protection = false

  parameters = [
    {
      name  = "character_set_client"
      value = "utf8"
    },
    {
      name  = "character_set_server"
      value = "utf8"
    }
  ]

  options = [
    {
      option_name = "MARIADB_AUDIT_PLUGIN"

      option_settings = [
        {
          name  = "SERVER_AUDIT_EVENTS"
          value = "CONNECT"
        },
        {
          name  = "SERVER_AUDIT_FILE_ROTATIONS"
          value = "37"
        },
      ]
    },
  ]
}

module "elastic_beanstalk_environment" {

  source                     = "git::https://github.com/cloudposse/terraform-aws-elastic-beanstalk-environment.git?ref=tags/0.31.0"
  namespace                  = var.namespace
  stage                      = var.stage
  name                       = var.name
  attributes                 = var.attributes
  tags                       = var.tags
  delimiter                  = var.delimiter
  description                = var.description
  region                     = var.region
  availability_zone_selector = var.availability_zone_selector
  dns_zone_id                = var.dns_zone_id

  wait_for_ready_timeout             = var.wait_for_ready_timeout
  elastic_beanstalk_application_name = var.eb_app_name
  environment_type                   = var.environment_type
  loadbalancer_crosszone             = var.loadbalancer_crosszone
  elb_scheme                         = var.elb_scheme
  tier                               = var.tier
  version_label                      = var.version_label
  force_destroy                      = var.force_destroy

  instance_type    = var.instance_type
  root_volume_size = var.root_volume_size
  root_volume_type = var.root_volume_type

  autoscale_min             = var.autoscale_min
  autoscale_max             = var.autoscale_max
  autoscale_measure_name    = var.autoscale_measure_name
  autoscale_statistic       = var.autoscale_statistic
  autoscale_unit            = var.autoscale_unit
  autoscale_lower_bound     = var.autoscale_lower_bound
  autoscale_lower_increment = var.autoscale_lower_increment
  autoscale_upper_bound     = var.autoscale_upper_bound
  autoscale_upper_increment = var.autoscale_upper_increment

  vpc_id                     = module.vpc.vpc_id
  loadbalancer_subnets       = module.subnets.public_subnet_ids
  application_subnets        = module.subnets.private_subnet_ids
  additional_security_groups = [module.vpc.vpc_default_security_group_id, module.db_sg.this_security_group_id]
  allowed_security_groups    = [module.db_sg.this_security_group_id]


  rolling_update_enabled  = var.rolling_update_enabled
  rolling_update_type     = var.rolling_update_type
  updating_min_in_service = var.updating_min_in_service
  updating_max_batch      = var.updating_max_batch

  healthcheck_url              = var.healthcheck_url
  application_port             = var.application_port
  extended_ec2_policy_document = "{\"Version\" : \"2012-10-17\",\"Statement\" : [{\"Effect\" : \"Allow\",\"Action\" : \"s3:*\",\"Resource\" : \"*\"},{\"Action\" : [\"sns:*\"],\"Effect\" : \"Allow\",\"Resource\" : \"*\"}]}"

  solution_stack_name = var.solution_stack_name
  env_vars = {
    "RDS_USERNAME" = module.db.this_db_instance_username,
    "RDS_PASSWORD" = module.db.this_db_instance_password,
    "RDS_HOSTNAME" = module.db.this_db_instance_address,
    "RDS_PORT"     = module.db.this_db_instance_port,
    "RDS_DB_NAME"  = module.db.this_db_instance_name
  }

}




# resource "aws_elasticache_cluster" "example" {
#   cluster_id           = "dbcache"
#   engine               = "memcached"
#   node_type            = "cache.t2.micro"
#   parameter_group_name = "default.memcached1.5"
#   num_cache_nodes      = 1
#   subnet_group_name    = "hacache"
#   security_group_ids   = ["sg-0e68fafbae4a2a08f"]
#   port                 = 11211
# }
