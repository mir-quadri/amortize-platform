provider "kind" {}

resource "kind_cluster" "default" {
  name            = var.cluster_name
  kubernetes_version = var.kubernetes_version
  wait_for_ready = true

  kind_config = yamlencode({
    apiVersion = "kind.x-k8s.io/v1alpha4"
    kind       = "Cluster"
    name       = var.cluster_name
    nodes = [
      {
        role = "control-plane"
      },
      {
        role = "worker"
      }
    ]
  })
}
