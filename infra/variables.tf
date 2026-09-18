variable "cluster_name" {
  description = "Name of the kind cluster"
  type        = string
  default     = "amortize-poc"
}

variable "kubernetes_version" {
  description = "Kubernetes version to use"
  type        = string
  default     = "v1.29.0"
}

variable "kubeconfig_path" {
  description = "Path where kubeconfig will be written"
  type        = string
  default     = "./kubeconfig"
}
