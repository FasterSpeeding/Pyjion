export DOTNET_VERSION=6.0.100
echo "Building Pyjion with .NET  $DOTNET_VERSION"
yum install -y wget && yum clean all
wget https://dotnetcli.azureedge.net/dotnet/Sdk/${DOTNET_VERSION}/dotnet-sdk-${DOTNET_VERSION}-linux-arm64.tar.gz
mkdir -p dotnet && tar zxf dotnet-sdk-${DOTNET_VERSION}-linux-arm64.tar.gz -C dotnet
export DOTNET_ROOT=/src/dotnet