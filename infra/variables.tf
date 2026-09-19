variable "cluster_name" {
  description = "Name of the kind cluster"
  type        = string
  default     = "amortize-poc"
}

variable "kubeconfig_path" {
  description = "Path where kubeconfig will be written"
  type        = string
  default     = "./kubeconfig"
}
