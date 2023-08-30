# Reusable Terraform Deployment Workflow
## terraform/github/automation/workflows
## [Resuable Workflow Github Repo](https://github.com/ukhan262/Resuable-Workflows)

This GitHub Actions workflow automates the deployment of Terraform configurations using HashiCorp Terraform, targeting Terraform Cloud or Terraform Enterprise workspaces. It supports planning and applying changes to your infrastructure based on your Terraform code.

## Workflow Inputs

- `tf_workspace_name` (optional): Name of the workspace in Terraform Cloud or Terraform Enterprise.
- `tf_version` (required): Version of Terraform to be used for deployment.
- `tf_organization` (required): Name of the Terraform organization.
- `run_apply` (default: "no"): Set to "yes" if the code needs to be deployed.
- `run_destroy` (default: "no"): Set to "yes" if the resources need to be destroyed.

## Workflow Secrets

- `tf_token` (required): Token for authenticating with Terraform Cloud or Terraform Enterprise.

## Permissions

The following permissions are required for this workflow:

- `id-token`: Write access
- `contents`: Read access

## Workflow Steps

1. **Print Inputs**: Print the input values for workspace name, Terraform version, and Terraform token.

2. **Checkout Repository**: Checkout the repository content.

3. **Set up Terraform**: Set up Terraform CLI using the specified version and token.

4. **Setup Remote Config Backend**: Create a configuration file for the remote backend specifying workspace details and organization.

5. **Terraform Init**: Initialize the Terraform project with the configured remote backend.

6. **Terraform Plan**: Generate a Terraform execution plan for changes to be applied.

7. **Terraform Apply**: Apply the changes to the infrastructure if `run_apply` is set to "yes".

8. **Terraform Destroy**: Destroy the changes to the infrastructure if `run_destroy` is set to "yes".

## Usage

1. Create a new GitHub workflow file (e.g., `.github/workflows/terraform-deployment.yml`) in your repository.

2. Copy and paste the workflow content from this `README.md` into the new workflow file.

3. Configure the required inputs, such as `tf_version`, `tf_organization`, and `tf_token`, in the workflow file.

4. Optionally, provide the `tf_workspace_name` if you want to deploy to a specific workspace.

5. Commit and push the changes to your repository.

Now, whenever you trigger the workflow, it will automatically set up Terraform, initialize the backend, create an execution plan, and deploy changes to your infrastructure if specified.

Feel free to modify and extend this workflow according to your project's requirements.

**Note:** Ensure that you protect sensitive information such as tokens and credentials using GitHub Secrets for a secure workflow.

For more information, refer to the [GitHub Actions documentation](https://docs.github.com/en/actions) and [HashiCorp Terraform documentation](https://learn.hashicorp.com/terraform).
