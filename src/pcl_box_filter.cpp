#define PCL_NO_PRECOMPILE

#include <ros/ros.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/pcl_macros.h>
#include <pcl/common/common.h>
#include <pcl/common/transforms.h>
#include <pcl/filters/crop_box.h>
#include <pcl/ModelCoefficients.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <jsk_recognition_msgs/BoundingBox.h>
#include <dynamic_reconfigure/server.h>
#include <repeatability_processing/BoxParamsConfig.h>

ros::Publisher pub;
ros::Publisher bbox_pub;
ros::Publisher target_plane_pub;
using PointT = pcl::PointXYZ;

std::string topic_name, frame_name;
float box_min_x, box_min_y, box_min_z, box_max_x, box_max_y, box_max_z;

// void callback(repeatability_processing::BoxParamsConfig &config, uint32_t level){
//   box_min_x = config.box_min_x;
//   box_max_x = config.box_max_x;
//   box_min_y = config.box_min_y;
//   box_max_y = config.box_max_y;
//   box_min_z = config.box_min_z;
//   box_max_z = config.box_max_z;
// }

void 
cloud_cb (const sensor_msgs::PointCloud2ConstPtr& input)
{


  sensor_msgs::PointCloud2 output;
  pcl::PointCloud<PointT>::Ptr input_cloud(new pcl::PointCloud<PointT>);
  pcl::PointCloud<PointT>::Ptr cloud_out(new pcl::PointCloud<PointT>);

  pcl::fromROSMsg(*input, *input_cloud);
  pcl::CropBox<PointT> cropBoxFilter;

  Eigen::Vector4f min_pt (box_min_x, box_min_y, box_min_z, 1);
  Eigen::Vector4f max_pt (box_max_x, box_max_y, box_max_z, 1);

  // Cropbox slighlty bigger then bounding box of points
  cropBoxFilter.setMin (min_pt);
  cropBoxFilter.setMax (max_pt);

  cropBoxFilter.setInputCloud (input_cloud);
  cropBoxFilter.setNegative(false);
  cropBoxFilter.filter (*cloud_out);

  // convert from PCL PointCloud to ROS PointCloud2
  pcl::toROSMsg(*cloud_out, output);
  pub.publish (output);

  // ----------------------------------------------------------------------------
  // publish the marker box visualization msg
  jsk_recognition_msgs::BoundingBox bbox_msg;
  bbox_msg.header.frame_id = frame_name;        // uses frame launch param
  bbox_msg.header.stamp = ros::Time::now();

  // pose
  bbox_msg.pose.position.x = (box_min_x + box_max_x)/2;
  bbox_msg.pose.position.y = (box_min_y + box_max_y)/2;
  bbox_msg.pose.position.z = (box_min_z + box_max_z)/2;
  bbox_msg.pose.orientation.x = 0.0;
  bbox_msg.pose.orientation.y = 0.0;
  bbox_msg.pose.orientation.z = 0.0;
  bbox_msg.pose.orientation.w = 1.0;

  // dims
  bbox_msg.dimensions.x = (box_max_x - box_min_x); // Length
  bbox_msg.dimensions.y = (box_max_y - box_min_y); // Width
  bbox_msg.dimensions.z = (box_max_z - box_min_z); // Height

  // labels
  bbox_msg.value = 1.0;
  bbox_msg.label = 0;

  // Publish the marker
  bbox_pub.publish(bbox_msg);
}

// -------------------------------------------------------------------
// ROS init, get static params, and start dynamic param server

int
main (int argc, char** argv)
{
  ros::init (argc, argv, "box_node");
  ros::NodeHandle nh;
  
  nh.getParam("/box_node/input_topic", topic_name);
  nh.getParam("/box_node/frame", frame_name);
  nh.getParam("/box_node/box_min_x", box_min_x);
  nh.getParam("/box_node/box_min_y", box_min_y);
  nh.getParam("/box_node/box_min_z", box_min_z);
  nh.getParam("/box_node/box_max_x", box_max_x);
  nh.getParam("/box_node/box_max_y", box_max_y);
  nh.getParam("/box_node/box_max_z", box_max_z);

  // dynamic_reconfigure::Server<repeatability_processing::BoxParamsConfig> server;
  // dynamic_reconfigure::Server<repeatability_processing::BoxParamsConfig>::CallbackType f;

  // f = boost::bind(&callback, _1, _2);
  // server.setCallback(f);

  ros::Subscriber sub = nh.subscribe (topic_name, 1, cloud_cb); 

  pub = nh.advertise<sensor_msgs::PointCloud2> ("/box_cropped_points", 1);
  bbox_pub = nh.advertise<jsk_recognition_msgs::BoundingBox>("box_filter_dimensions", 1);

  ros::spin ();
}