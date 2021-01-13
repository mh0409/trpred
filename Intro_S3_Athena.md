# Using AWS: S3 and Athena

Created: Nov 25, 2020 11:26 AM
Created By: Maria Jose Herrera
Last Edited By: Maria Jose Herrera
Last Edited Time: Dec 4, 2020 4:20 PM

# Overview

The goal of this walkthrough is to give high-level instructions on how to upload documents to AWS Simple Storage Service (S3 — a web-based object storage service), and to create a SQL-queryable database using another AWS service, Athena. 

For introductory information, refer to the AWS docs listed below:

- [AWS](https://docs.aws.amazon.com/AmazonS3/latest/dev/Introduction.html)
- [Athena](https://docs.aws.amazon.com/athena/latest/ug/what-is.html)

In the documentation below, I use the GUI (or online) S3 and Athena interface to set up services, but this can also be done through the command line using [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) (Command Line Interface) and using [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). 

**Editorial note:** Personally, I think it's best to first use the GUI if this is the first / one of a few times you've set up S3. Once the you understand the process and are looking to speed up your workflow, look into the AWS modules (`awscli` and `boto3` , which can both be `pip install`ed)

# Step 1: Getting S3 up and running

- Set up AWS S3 bucket
    - Region
    - Most of the time, go with default options the whole way across
    - For more detail, look at [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)
    - Consider creating bucket in London region for regulatory reasons and blocking public access for privacy reasons
- Upload files to S3 bucket
    - Can make tables only based on 1 directory
- Cost:
    - Based on amount of storage used and number of put/pull requests

    Currently, about 110 GB for all data (both raw and processed) at a rate for $0.024 per GB. More detailed cost info can be found [here](https://aws.amazon.com/s3/pricing/?nc1=h_ls). This varies by the type of S3 bucket and the frequency of access.

- Manage permissions to S3 bucket
    - For an instance where you're working with a few close collaborators (as most researchers are), probably most straightforward to give access using ACL.
        - This allows one to grant (read or write) access at the bucket level and seemed to make the most sense at for this project, for example
        - To share the S3 bucket, you need the canonical ID for the other user.

# Step 2: Set up Athena to query S3 bucket

- Create a database
    - 
- Create a table
- Using the GUI
- Using a SQL query
- Considerations:
    - Files in S3 bucket are assumed to be CSV files where one row is one observation / item
    - Text data -
        - Consider OpenCSVSerDe (instead of deafult LazySerDe if data may contain a newline character in a column (i.e. problem can arise in how Athena reads in the table for a CSV file) is found in a column
        - Processed data must be cleaned of newline characters ("\n") before being added into Athena, otherwise newlines with break the CSV format and lead to a lot of weirdness
- Cost:
    - For my bucket, cost is allocated to whomever runs the query
    - [Link](https://aws.amazon.com/athena/pricing/) to pricing info

    Add more detailed cost info / screenshot of when I set the cost to be paid by whomever runs the query

# Step 3: Use Athena in your program of choice

- [Setting up Athena with R or R Studio](https://aws.amazon.com/blogs/big-data/running-r-on-amazon-athena/)
- [Setting up Athena with Python using Boto3](https://medium.com/dataseries/automating-athena-queries-from-s3-with-python-and-save-it-as-csv-8917258b1045)