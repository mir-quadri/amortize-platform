output "kubeconfig_path" {
  description = "Path to the kubeconfig file written by the kind provider"
  value       = kind_cluster.default.kubeconfig_path
}

output "cluster_name" {
  description = "Name of the created kind cluster"
  value       = kind_cluster.default.name
}
