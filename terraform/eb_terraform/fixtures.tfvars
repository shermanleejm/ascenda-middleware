region = "ap-southeast-1"

availability_zones = ["ap-southeast-1a", "ap-southeast-1b"]

namespace = "eg"

stage = "test"

name = "demo-in-class"

description = "Test elastic-beanstalk-environment"

tier = "WebServer"

environment_type = "LoadBalanced"

# loadbalancer_type = "application"
eb_app_name = "itsa_backend"

availability_zone_selector = "Any 2"

instance_type = "t2.micro"

autoscale_min = 2

autoscale_max = 4

wait_for_ready_timeout = "20m"


force_destroy = true

rolling_update_enabled = true

rolling_update_type = "Health"

updating_min_in_service = 0

updating_max_batch = 1

healthcheck_url = "/"

application_port = 80

root_volume_size = 8

root_volume_type = "gp2"

autoscale_measure_name = "CPUUtilization"

autoscale_statistic = "Average"

autoscale_unit = "Percent"

autoscale_lower_bound = 20

autoscale_lower_increment = -1

autoscale_upper_bound = 80

autoscale_upper_increment = 1
 
elb_scheme = "public"

loadbalancer_crosszone = true

// https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html
// https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html#platforms-supported.docker
solution_stack_name = "64bit Amazon Linux 2 v3.1.2 running Python 3.7"

version_label = "itsa_backend-2020-11-08T08-55-21"

dns_zone_id = "Z3SO0TKDDQ0RGG"

// https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-general.html
additional_settings = [
  {
    namespace = "aws:elasticbeanstalk:environment:process:default"
    name      = "StickinessEnabled"
    value     = "true"
  },
  {
    namespace = "aws:elasticbeanstalk:managedactions"
    name      = "ManagedActionsEnabled"
    value     = "false"
  }
]



