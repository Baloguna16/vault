# No Secrets Here

This should always remain a private repository. No secrets will be uploaded. Rather, the encrypted secrets will be stored in a secret location on my computer... SHHHH! No secrets here.

### Get Started

Manage your secrets with one secure key...

From the root directory:

`cd src`
`virtualenv env`

### Features

The features provided by this command line tool:
* Encryption and decryption of provided data (symmetric)
* Data retrieval by label

### How to Use

Configure the environment:

`cd src`
`touch .env`

In your .env file:

  source env/bin/activate

  export MAX_ATTEMPTS=<NUM>
  export COOLDOWN_TIME=<NUM>
  export STORAGE_FILE=<FILENAME>

  pip3 install -r requirements.txt
  pip3 install -e .

`source .env`

To generate access key:

`vault init`

**Note Make sure you copy this key somewhere!**

To write to storage:

`vault encrypt --label=<your-label> --data=<your-secret>`

Use the label to call for that data again when you need it.

`vault decrypt --label=<label-of-your-requested-secret>`

You'll need to provide the exact name of the label that you are requesting. Though, this is hopefully easier than remembering the secret...
