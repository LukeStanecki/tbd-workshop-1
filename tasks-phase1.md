IMPORTANT ❗ ❗ ❗ Please remember to destroy all the resources after each work session. You can recreate infrastructure by creating new PR and merging it to master.
  
![img.png](doc/figures/destroy.png)

1. Authors:

   ***9***

   ***[link to forked repo](https://github.com/LukeStanecki/tbd-workshop-1)***
   
2. Follow all steps in README.md.

3. Select your project and set budget alerts on 5%, 25%, 50%, 80% of 50$ (in cloud console -> billing -> budget & alerts -> create buget; unclick discounts and promotions&others while creating budget).

  ![img.png](doc/figures/discounts.png)

4. From avaialble Github Actions select and run destroy on main branch.
   
5. Create new git branch and:
    1. Modify tasks-phase1.md file.
    
    2. Create PR from this branch to **YOUR** master and merge it to make new release. 

    
    ***place the screenshot from GA after succesfull application of release***
    ![after merge](images/phase1-task6p2/task6ii-po mergu.png)

6. Analyze terraform code. Play with terraform plan, terraform graph to investigate different modules.

    ***describe one selected module and put the output of terraform graph for this module here***
   
7. Reach YARN UI
   
   ## SSH Tunnelowanie do Klastrowego Interfejsu Użytkownika

Aby uzyskać dostęp do interfejsu użytkownika YARN w klastrze (port 8088), nalezy skonfigurować tunel SSH, który przekieruje port lokalny na port klastra. Polecenie w terminalu:

```bash
gcloud compute ssh tbd-cluster-m \
    --project=tbd-2024z-313787 -- \
    -L 1080:tbd-cluster-m:8088 -N -n
```

![yarnui.png](images/yarnui/yarnui.png)
   
8.  Draw an architecture diagram (e.g. in draw.io) that includes:
    1. VPC topology with service assignment to subnets
    2. Description of the components of service accounts
    3. List of buckets for disposal
    4. Description of network communication (ports, why it is necessary to specify the host for the driver) of Apache Spark running from Vertex AI Workbech
  
    ***place your diagram here***

9.  Create a new PR and add costs by entering the expected consumption into Infracost
For all the resources of type: `google_artifact_registry`, `google_storage_bucket`, `google_service_networking_connection`
create a sample usage profiles and add it to the Infracost task in CI/CD pipeline. Usage file [example](https://github.com/infracost/infracost/blob/master/infracost-usage-example.yml) 

   ***place the expected consumption you entered here***
    https://github.com/LukeStanecki/tbd-workshop-1/blob/1b4586860788c12dd3ab35783f5c5b8eb3d24026/infracost-usage.yml#L1-L14 

    https://github.com/LukeStanecki/tbd-workshop-1/blob/77a2e69954c6c8618e1385c79339925aa29f0ba3/.github/workflows/infracost.yml#L1-L65
    '''yml
        name: Tech Tests

        on: [pull_request]
        permissions: read-all

        jobs:
        iac_checks:
            runs-on: ubuntu-latest
            permissions:
            contents: read
            id-token: write
            pull-requests: write
            security-events: write
            actions: read

            steps:
            - uses: 'actions/checkout@v3'

            - uses: hadolint/hadolint-action@v3.1.0
                with:
                recursive: true
                verbose: true

            # Authenticate with Google Cloud using Workload Identity Federation
            - id: 'auth'
                name: 'Authenticate to Google Cloud'
                uses: 'google-github-actions/auth@v1'
                with:
                token_format: 'access_token'
                workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER_NAME }}
                service_account: ${{ secrets.GCP_WORKLOAD_IDENTITY_SA_EMAIL }}

            - name: Set up Infracost
                uses: infracost/actions/setup@v2.1.0
                with:
                api-key: ${{ secrets.INFRACOST_API_KEY }}

            # Run Infracost to generate the baseline cost estimate
            - name: Generate Infracost baseline cost estimate
                run: |
                infracost breakdown --path="." \
                                    --usage-file="infracost-usage.yml" \
                                    --format=json \
                                    --out-file=/tmp/infracost-base.json

            # Checkout PR branch again
            - name: Checkout PR branch
                uses: actions/checkout@v3

            # Run Infracost diff to compare PR changes with baseline
            - name: Generate Infracost diff
                run: |
                infracost diff --path="." \
                                --compare-to=/tmp/infracost-base.json \
                                --format=json \
                                --out-file=/tmp/infracost.json

            # Post Infracost diff as a comment in the PR
            - name: Post Infracost comment
                run: |
                infracost comment github --path=/tmp/infracost.json \
                                        --repo=$GITHUB_REPOSITORY \
                                        --github-token=${{secrets.GITHUB_TOKEN}} \
                                        --pull-request=${{github.event.pull_request.number}} \
                                        --behavior=update
    
    
   ***place the screenshot from infracost output here***

10.  Create a BigQuery dataset and an external table using SQL
    
    ***place the code and output here***
   
    ***why does ORC not require a table schema?***

  
11. Start an interactive session from Vertex AI workbench:

    ***place the screenshot of notebook here***
   
12. Find and correct the error in spark-job.py

    ***describe the cause and how to find the error***

13. Additional tasks using Terraform:

    1. Add support for arbitrary machine types and worker nodes for a Dataproc cluster and JupyterLab instance

    ***place the link to the modified file and inserted terraform code***
    
    3. Add support for preemptible/spot instances in a Dataproc cluster

    ***place the link to the modified file and inserted terraform code***
    
    3. Perform additional hardening of Jupyterlab environment, i.e. disable sudo access and enable secure boot
    
    ***place the link to the modified file and inserted terraform code***

    4. (Optional) Get access to Apache Spark WebUI

    ***place the link to the modified file and inserted terraform code***
