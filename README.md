# Payment Gateway Integration and Files Uploading System
## 1. Project Setup Instructions

Once system dependencies and Python are set:

#### 1.1 Create a Virtual Environment and Install Project Requirements:

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### 2.2set the .env from example.env
You are now ready to start development or run the project.

## Project Run
step-1: sudo service redis-server start
step-2: celery -A aamarPay worker --loglevel=info

## API endpoints
#### User Registration  
**POST** `/registration/`  
Create a new user account. Returns JWT access and refresh tokens on success.

#### User Login (Token Obtain)  
**POST** `/token/`  
Authenticate user credentials and receive JWT access and refresh tokens.

#### Token Refresh  
**POST** `/atoken/refresh/`  
Send a valid refresh token to get a new access token without re-authenticating.

#### 1. Files API
**URL:** `/api/files/`  
**Methods:** `GET`,  `PATCH`, `DELETE`  
**Permissions:** Authenticated users only  

- **GET**  
  - Retrieve all files, or a specific file by providing `file_id` as a query parameter.
  - If You are normal user, only get your uploaded file or superuser get all files
  - Example:  
    ```
    GET /api/files/?file_id=1
    GET /api/files/
    ```


- **PATCH**  
  - Partially update a uploaded file using the `file_id` query parameter and the fields to update in the request body.  
  - Example:  
    ```
    PATCH /api/files/?file_id=1
    Body: { "filename": "abc.txt" }
    ```

- **DELETE**  
  - Delete a file by its `file_id`.  
  - Example:  
    ```
    DELETE /api/files/?file_id=1
    ```

#### 2. File Upload
**URL:** `/api/upload/`  
**Methods:** `POST`  
**Permissions:** Authenticated users only 
- Example:  
    ```
    POST /api/upload/
    Body: { "file": given a file } here attach a file,from this file automated get filename,word count using celery task and create the ActivityLog with values
    ```
#### 1. Activity List
**URL:** `/api/activity/`  
**Methods:** `GET`  
**Permissions:** Authenticated users only 
- **GET**  
  - Retrieve all activity
  - If You are normal user, only get your activity  or superuser get all activity
  - Example:  
    ```
    GET /api/activity/
    ```

#### 3. Transactions or payment history
**URL:** `/api/transactions/`  
**Methods:** `GET`  
**Permissions:** Authenticated users only 
- **GET**  
  - Retrieve all transaction, or a specific transaction by providing `transaction_id` as a query parameter.
  - If You are normal user, only get your transaction history or superuser get all transaction
  - Example:  
    ```
    GET /api/transactions/?transaction_id=1
    GET /api/transactions/
    ```

- **DELETE**  
  - Delete a file by its `transaction_id`.  
  - Example:  
    ```
    DELETE /api/transactions/?transaction_id=1
    ```

#### 3.Payment
**URL:** `/api/initiate-payment/`  
**Methods:** `POST`  
**Permissions:** Authenticated users only 
- **POST**  
  - I have created a aamarPay payment request by taking data from some users. If you go to the file upload option on the dashboard,
  - there will be a button on the top right, this button is Pay Fast, so when you click on it, I am taking some data from
  - the user and requesting payment(using /api/initiate-payment/) with that. After payment, the button is ready for the upload file, then the user uploads the file.
  - Example:  
    ```
    POST /api/initiate-payment/
    
    ```


