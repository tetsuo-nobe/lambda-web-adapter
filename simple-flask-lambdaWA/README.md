# Lambda Web Adapter 
- Lambda Web Adapter を使用した Lambda 関数を作成するには、コンテナ形式でのデプロイが必要。よって Amazon ECR の使用が必須となる。
  - **Dockerfile に COPY 文を 1 つ追加するだけでよい**
- 参考ドキュメント
  - [Lambda Web Adapter でウェブアプリを (ほぼ) そのままサーバーレス化する](https://aws.amazon.com/jp/builders-flash/202301/lambda-web-adapter/)
  - [AWS Lambda の上でいろんなWEB フレームワークを動かそう！](https://speakerdeck.com/_kensh/web-frameworks-on-lambda)

## コンテナイメージの作成
- コンテナイメージのビルド
```
docker build -t simple-flask-lambd .
```

- コンテナのテスト実行
```
docker run -dt -p 8080:8080 simple-flask-lambdawa
```

- コンテナの　ID 確認
```
docker ps
```

- コンテナの停止
```
docker stop <CONTAINER ID>
```

## コンテナイメージを Amazon ECR へ push
- リージョンとアカウント ID の設定
```
REGION=$(aws configure get region)
ACCOUNTID=$(aws sts get-caller-identity --output text --query Account)
```

- Amazon ECR のリポジトリ作成
```
aws ecr create-repository \
    --repository-name simple-flask-lambdawa \
    --region ${REGION}
```

- Amazon ECR 用にイメージタグを設定
```
docker tag simple-flask-lambdawa:latest \
  ${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com/simple-flask-lambdawa:latest
```

- Amazon ECR にログイン
```
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com
```

- Amazon ECR へ push
```
docker push ${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com/simple-flask-lambdawa:latest
```

- イメージの DIGEST を取得
```
DIGEST=$(aws ecr list-images --repository-name simple-flask-lambdawa --out text --query 'imageIds[?imageTag==`latest`].imageDigest')
```

- Lambda 関数 (Web Adapter) の作成
```
aws lambda create-function \
     --function-name simple-flask-lambdawa  \
     --package-type Image \
     --code ImageUri=${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com/simple-flask-lambdawa@${DIGEST} \
     --role arn:aws:iam::${ACCOUNTID}:role/my-lambda-bedrock-s3-role
```

- API Gateway と統合する場合
  - プロキシ統合を指定する
  - URLのパスは、Flask アプリケーションで指定しているパスと合わせる 
