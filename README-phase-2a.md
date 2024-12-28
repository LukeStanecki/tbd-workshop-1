IMPORTANT ❗ ❗ ❗ Please remember to destroy all the resources after each work session. You can recreate infrastructure by creating new PR and merging it to master.

![img.png](doc/figures/destroy.png)

1. The goal of this phase is to create infrastructure, perform benchmarking/scalability tests of sample three-tier lakehouse solution and analyze the results using:
* [TPC-DI benchmark](https://www.tpc.org/tpcdi/)
* [dbt - data transformation tool](https://www.getdbt.com/)
* [GCP Composer - managed Apache Airflow](https://cloud.google.com/composer?hl=pl)
* [GCP Dataproc - managed Apache Spark](https://spark.apache.org/)
* [GCP Vertex AI Workbench - managed JupyterLab](https://cloud.google.com/vertex-ai-notebooks?hl=pl)

Worth to read:
* https://docs.getdbt.com/docs/introduction
* https://airflow.apache.org/docs/apache-airflow/stable/index.html
* https://spark.apache.org/docs/latest/api/python/index.html
* https://medium.com/snowflake/loading-the-tpc-di-benchmark-dataset-into-snowflake-96011e2c26cf
* https://www.databricks.com/blog/2023/04/14/how-we-performed-etl-one-billion-records-under-1-delta-live-tables.html

2. Authors:

   ***z9***
   
   Łukasz Stanecki
   
   Krzysztof Błażejewski
   
   Alina Yermakova

   ***[link to forked repo](https://github.com/LukeStanecki/tbd-workshop-1)***

3. Sync your repo with https://github.com/bdg-tbd/tbd-workshop-1.

![task3.png](images/phase_2a/task_3/task3.png)

4. Provision your infrastructure.

    a) setup Vertex AI Workbench `pyspark` kernel as described in point [8](https://github.com/bdg-tbd/tbd-workshop-1/tree/v1.0.32#project-setup) 

    ![task4a.png](images/phase_2a/task_4/task4_a.png)

    b) upload [tpc-di-setup.ipynb](https://github.com/bdg-tbd/tbd-workshop-1/blob/v1.0.36/notebooks/tpc-di-setup.ipynb) to 
the running instance of your Vertex AI Workbench

   ![task4b.png](images/phase_2a/task_4/task4_b.png)

5. In `tpc-di-setup.ipynb` modify cell under section ***Clone tbd-tpc-di repo***:

   a)first, fork https://github.com/mwiewior/tbd-tpc-di.git to your github organization.

   b)create new branch (e.g. 'notebook') in your fork of tbd-tpc-di and modify profiles.yaml by commenting following lines:
   ```  
        #"spark.driver.port": "30000"
        #"spark.blockManager.port": "30001"
        #"spark.driver.host": "10.11.0.5"  #FIXME: Result of the command (kubectl get nodes -o json |  jq -r '.items[0].status.addresses[0].address')
        #"spark.driver.bindAddress": "0.0.0.0"
   ```
   This lines are required to run dbt on airflow but have to be commented while running dbt in notebook.

   ![task5b.png](images/phase_2a/task_5/task_5b.png)

   c)update git clone command to point to ***your fork***.

 


6. Access Vertex AI Workbench and run cell by cell notebook `tpc-di-setup.ipynb`.

    a) in the first cell of the notebook replace: `%env DATA_BUCKET=tbd-2023z-9910-data` with your data bucket.

    ![task6a.png](images/phase_2a/task_6/task_6a.png)


   b) in the cell:
         ```%%bash
         mkdir -p git && cd git
         git clone https://github.com/mwiewior/tbd-tpc-di.git
         cd tbd-tpc-di
         git pull
         ```
      replace repo with your fork. Next checkout to 'notebook' branch.

      ![task6b.png](images/phase_2a/task_6/task_6b.png)

   
    c) after running first cells your fork of `tbd-tpc-di` repository will be cloned into Vertex AI  enviroment (see git folder).

    d) take a look on `git/tbd-tpc-di/profiles.yaml`. This file includes Spark parameters that can be changed if you need to increase the number of executors and
  ```
   server_side_parameters:
       "spark.driver.memory": "2g"
       "spark.executor.memory": "4g"
       "spark.executor.instances": "2"
       "spark.hadoop.hive.metastore.warehouse.dir": "hdfs:///user/hive/warehouse/"
  ```

   ![task6d.png](images/phase_2a/task_6/task_6d.png)

7. Explore files created by generator and describe them, including format, content, total size.

   ***Files desccription***

   ![task7_1.png](images/phase_2a/task_7/task_7_1.png)
   ![task7_2.png](images/phase_2a/task_7/task_7_2.png)

   [Full digen report](phase2_data/task_7/task7_digen_report.txt)

   ![task_7_batch1.png](images/phase_2a/task_7/task_7_batch1.png)

   [Full Batch1](phase2_data/task_7/batch1.txt)

   ![task_7_batch2.png](images/phase_2a/task_7/task_7_batch2.png)

   [Full Batch2](phase2_data/task_7/batch2.txt)

   ![task_7_batch3.png](images/phase_2a/task_7/task_7_batch3.png)

   [Full Batch3](phase2_data/task_7/batch3.txt)


8. Analyze tpcdi.py. What happened in the loading stage?

   ***Your answer***

   ![task8.png](images/phase_2a/task_8/task_8.png)

   [tpcdi.py file](https://github.com/LukeStanecki/tbd-tpc-di/blob/main/tpcdi.py)

9. Using SparkSQL answer: how many table were created in each layer?

   ***SparkSQL command and output***

   ![task9_1.png](images/phase_2a/task_9/task9_1.png)
   ![task9_2.png](images/phase_2a/task_9/task9_2.png)
   ![task9_3.png](images/phase_2a/task_9/task9_3.png)

   [commands and outputs](phase2_data/task_9/task9.txt)

10. Add some 3 more [dbt tests](https://docs.getdbt.com/docs/build/tests) and explain what you are testing. ***Add new tests to your repository.***

   ***Code and description of your tests***

11. In main.tf update
   ```
   dbt_git_repo            = "https://github.com/mwiewior/tbd-tpc-di.git"
   dbt_git_repo_branch     = "main"
   ```
   so dbt_git_repo points to your fork of tbd-tpc-di. 

12. Redeploy infrastructure and check if the DAG finished with no errors:

***The screenshot of Apache Aiflow UI***
