from setuptools import setup, find_packages

setup(
    name='lemon-auto-saver',
    version='1.0.0',
    description='A tool for automatic saving of documents in various applications.',
    long_description=open('README.md', 'r', encoding = 'utf-8').read(),
    long_description_content_type='text/markdown',
    author='啊米诺斯',
    author_email='1154330861@qq.com',
    url='https://github.com/GoldenStain/lemon-auto-saver',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyautogui',
        'psutil',
        'pywinauto',
        'pygetwindow'
    ],
    entry_points={
        'console_scripts': [
            'lemon-auto-saver=lemon_auto_saver.__main__:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)