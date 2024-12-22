# Azure DevOps Pipeline Template for Packer Builds
## azuredevops/pipelines/templates/packer
This Azure DevOps pipeline template designed for automating Packer builds to create and manage images across various environments. The pipeline leverages reusable parameters, dynamic stage creation, and automated cleanup tasks.


---

## Key Features

- **Dynamic Stage Generation**: Automatically creates pipeline stages for each Packer template defined in the parameters.
- **Parameterized Configurations**: Enables flexibility in defining variables and dependencies for each Packer build.
- **Automated Packer Setup**: Installs and configures Packer as part of the pipeline steps.
- **Azure Integration**: Supports Azure resource management for image builds and optional cleanup.

---

## Pipeline Overview

The pipeline dynamically generates stages based on the list of Packer templates passed as a parameter. Each stage includes the following steps:

1. **Install Packer**: Ensures Packer is installed and ready for use.
2. **Initialize Packer Templates**: Prepares the Packer templates for execution.
3. **Run Packer Build**: Executes the Packer build process using input variables.
4. **Optional Azure Cleanup**: Removes unused Azure images after the build process.

---

## YAML Structure

### Parameters

```yaml
parameters:
  # List of templates for Packer builds
  - name: templates
    type: object
    default: []
```

- **`templates`**: A list of objects, each representing a Packer build template. Each object can include:
  - `templateName`: The name of the Packer template.
  - `packerTemplatePath`: The path to the Packer template file.
  - `dependsOnStage`: (Optional) Stage dependencies.
  - `condition`: (Optional) Conditions for running the stage.
  - `variableGroup`: (Optional) Variable group for custom variables.
  - `clientId`, `clientSecret`, `tenantId`, `subscriptionId`: Azure credentials.
  - `imageName`, `imageVersion`: Image details.
  - `azureServiceConnection`: Azure service connection name.
  - `resourceGroup`: Azure resource group.

### Stages

```yaml
stages:
  - ${{ each template in parameters.templates }}:
      - stage: ${{ lower(replace(replace(template.templateName, '-', '_'), ' ', '_')) }}_packer_build
        displayName: "Packer Build for ${{ template.templateName }}"
        dependsOn: ${{ template.dependsOnStage }}
        condition: and(succeeded(), ${{ template.condition }})
        jobs:
          - job: build_${{ lower(replace(replace(template.templateName, '-', '_'), ' ', '_')) }}
            timeoutInMinutes: 360
            displayName: "Packer Build Job for ${{ template.templateName }}"
            variables:
              - group: ${{ template.variableGroup }}
            steps:
              - task: CmdLine@2
                displayName: Install Packer
                inputs:
                  script: |
                    curl -o packer.zip https://releases.hashicorp.com/packer/1.10.2/packer_1.10.2_windows_amd64.zip
                    tar -xf packer.zip
                    move packer.exe C:\packer
                    set PATH=C:\packer;%PATH%
                    echo "Packer Version:"
                    packer --version
              - task: CmdLine@2
                displayName: Packer Init
                inputs:
                  script: |
                    cd ${{ template.packerTemplatePath }}
                    packer init .
              - task: CmdLine@2
                displayName: Packer Build
                inputs:
                  script: |
                    cd ${{ template.packerTemplatePath }}
                    packer build ^
                      -var="client_id=${{ template.clientId }}" ^
                      -var="client_secret=${{ template.clientSecret }}" ^
                      -var="tenant_id=${{ template.tenantId }}" ^
                      -var="subscription_id=${{ template.subscriptionId }}" ^
                      -var="image_version=${{ template.imageVersion }}" ^
                      -var="image_name=${{ template.imageName }}" ^
                      -force .
              - task: AzureCLI@2
                displayName: Azure Image Cleanup
                inputs:
                  azureSubscription: ${{ template.azureServiceConnection }}
                  scriptType: pscore
                  scriptLocation: inlineScript
                  inlineScript: |
                    az image delete --name ${{ template.imageName }} --resource-group ${{ template.resourceGroup }} --subscription ${{ template.subscriptionId }}
```

---

## How to Use

1. **Define Templates**: Populate the `templates` parameter with a list of Packer build configurations.
2. **Configure Variables**: Ensure all required Azure credentials and Packer template variables are correctly set.
3. **Run the Pipeline**: Trigger the Azure DevOps pipeline. Stages will be dynamically created for each Packer template.
4. **Review Outputs**: Verify the Packer builds and manage resulting resources in Azure.

---

## Example Parameters

```yaml
parameters:
  templates:
    - templateName: "Ubuntu-Base-Image"
      packerTemplatePath: "packer/templates/ubuntu"
      dependsOnStage: ""
      condition: "true"
      variableGroup: "UbuntuImageVars"
      clientId: "your-client-id"
      clientSecret: "your-client-secret"
      tenantId: "your-tenant-id"
      subscriptionId: "your-subscription-id"
      imageName: "ubuntu-base-image"
      imageVersion: "1.0.0"
      azureServiceConnection: "AzureServiceConnectionName"
      resourceGroup: "ResourceGroupName"
```

---

## Future Enhancements

- Add support for other cloud providers (e.g., AWS, GCP).
- Implement automated testing for Packer templates.
- Enhance error handling and logging.

---

## Conclusion

This Azure DevOps pipeline template provides a robust and scalable solution for managing Packer builds. Its dynamic and modular design simplifies the process of creating images, making it an ideal choice for teams focused on infrastructure automation.

Feel free to adapt this template to your specific requirements and share your experiences! 🚀
