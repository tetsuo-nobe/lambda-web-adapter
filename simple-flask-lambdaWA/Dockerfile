# Pythonの公式Slimイメージをベースとして使用
FROM python:3.8-slim

# Lambda Web Adapter
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.5.0 /lambda-adapter /opt/extensions/lambda-adapter

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピーし、インストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# アプリケーションのファイルをコピー
COPY . .

# コンテナの8080番ポートを開放
EXPOSE 8080

# コンテナ起動時にFlaskアプリケーションを実行
CMD ["python", "app.py"]