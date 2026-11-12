# Reticulum for the dev setup: Python's rnsd with a shared instance and no
# interfaces (offline). retifs never brings its own Reticulum: this stands in
# for the one a machine already has (Prns, rnsd, ...).
FROM python:3.13-slim
RUN pip install --no-cache-dir rns
RUN mkdir -p /root/.reticulum && printf '[reticulum]\n  enable_transport = No\n  share_instance = Yes\n\n[interfaces]\n' > /root/.reticulum/config
CMD ["rnsd", "-v"]
