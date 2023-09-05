FROM python:3.9-bookworm

RUN pip3 install ipykernel
RUN pip3 install dash
RUN pip3 install dash_core_components
RUN pip3 install dash_html_components
RUN pip3 install pandas
RUN pip3 install dash-bootstrap-components
RUN pip3 install scikit-learn
RUN pip3 install XGBoost
RUN pip3 install numpy
RUN pip3 install plotly
RUN pip3 install seaborn
RUN pip3 install ppscore

COPY ./code /ml2023/code/

CMD tail -f /dev/null