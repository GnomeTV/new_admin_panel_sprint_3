AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttribute'
                'SimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLength'
                'Validator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPassword'
                'Validator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPassword'
                'Validator',
    },
]
