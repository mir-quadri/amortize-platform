output "kubeconfig_path" {
  description = "Path to the kubeconfig file"
  value       = var.kubeconfig_path
}

output "cluster_name" {
  description = "Name of the created kind cluster"
  value       = kind_cluster.default.name
}

output "kubeconfig" {
  description = "Kubeconfig for the cluster"
  value       = kind_cluster.default.kubeconfig
  sensitive   = true
}
