# 搶票雞巴人

## For Users

### Installation

```
pip install --upgrade setuptools wheel
pip install -r requirements.txt
```

### Execution

```
python app.py -h
```

### Sample Command

```
python app.py \
    --facebook_account abc@gmail.com \
    --facebook_password my_password_123 \
    --page https://tixcraft.com/activity/detail/24_asmrmaxxx
```

## For Developers

### Updating the packages

```
pip freeze > requirements.txt
```

In pycharm go to Tools -> Sync Python Requirements. There's a 'Remove unused requirements' checkbox.

## Troubleshooting

## Something went wrong when logging to facebook page

Please go back to the previous page, and the web app will continue

If that cannot be resolved, then close and restart another web app