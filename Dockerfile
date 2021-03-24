FROM python:3.9.2-slim-buster
RUN python3 -m pip install selenium \
    && python3 -m pip install pyyaml \
    && python3 -m pip install loguru \
    && python3 -m pip install apscheduler \
    && python3 -m pip install pillow \
    && python3 -m pip install baidu-aip
WORKDIR /ptqiandao
COPY qiandao.py .
COPY utils ./utils
RUN ls -la ./*
ENTRYPOINT [ "python3" ]
CMD [ "/ptqiandao/qiandao.py" ] 