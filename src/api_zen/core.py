import logging
import time
from typing import Any, Dict, Optional, Union

import httpx
import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ApiZen")

class ApiZenError(Exception):
    """Classe base para erros da ApiZen."""
    pass

class ApiZenHttpError(ApiZenError):
    """Erro lançado quando uma requisição HTTP falha (status 4xx ou 5xx)."""
    def __init__(self, message, status_code=None, response_data=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class ApiZenConfig:
    """Configurações globais opcionais para a biblioteca."""
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries

class BaseApiZen:
    """Base para clientes de API Síncronos e Assíncronos."""
    def __init__(self, base_url: str = "", headers: dict = None, timeout: int = 10, max_retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.max_retries = max_retries

    def _get_url(self, endpoint: str) -> str:
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}"

class ApiZen(BaseApiZen):
    """
    Cliente de API Síncrono robusto e fácil de usar.
    """
    def __init__(self, base_url: str = "", headers: dict = None, timeout: int = 10, max_retries: int = 3):
        super().__init__(base_url, headers, timeout, max_retries)
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def set_token(self, token: str, scheme: str = "Bearer"):
        """Define o token de autenticação nos headers."""
        self.session.headers.update({"Authorization": f"{scheme} {token}"})
        logger.info(f"Token de autenticação ({scheme}) configurado.")

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = self._get_url(endpoint)
        
        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.Timeout)),
            reraise=True
        )
        def send_request():
            logger.info(f"Chamando {method} em: {url}")
            start_time = time.time()
            try:
                kwargs.setdefault("timeout", self.timeout)
                response = self.session.request(method, url, **kwargs)
                duration = time.time() - start_time
                
                logger.info(f"Resposta: {response.status_code} ({duration:.2f}s)")
                response.raise_for_status()
                return response.json() if response.content else None
            except requests.exceptions.HTTPError as e:
                logger.error(f"Erro HTTP na requisição: {e}")
                raise ApiZenHttpError(str(e), status_code=e.response.status_code, response_data=e.response.text)
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro de rede/timeout na requisição: {e}")
                raise ApiZenError(str(e))

        return send_request()

    def get(self, endpoint: str, params: dict = None, **kwargs):
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: dict = None, json: dict = None, **kwargs):
        return self._request("POST", endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint: str, data: dict = None, json: dict = None, **kwargs):
        return self._request("PUT", endpoint, data=data, json=json, **kwargs)

    def patch(self, endpoint: str, data: dict = None, json: dict = None, **kwargs):
        return self._request("PATCH", endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)
    
    def head(self, endpoint: str, **kwargs):
        return self._request("HEAD", endpoint, **kwargs)

    def options(self, endpoint: str, **kwargs):
        return self._request("OPTIONS", endpoint, **kwargs)

class AsyncApiZen(BaseApiZen):
    """
    Cliente de API Assíncrono moderno e resiliente.
    """
    def __init__(self, base_url: str = "", headers: dict = None, timeout: int = 10, max_retries: int = 3):
        super().__init__(base_url, headers, timeout, max_retries)
        self.client_kwargs = {
            "base_url": self.base_url,
            "headers": self.headers,
            "timeout": self.timeout
        }

    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = self._get_url(endpoint)

        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException)),
            reraise=True
        )
        async def send_async_request():
            async with httpx.AsyncClient(**self.client_kwargs) as client:
                logger.info(f"Chamando (Async) {method} em: {url}")
                start_time = time.time()
                try:
                    response = await client.request(method, endpoint, **kwargs)
                    duration = time.time() - start_time
                    logger.info(f"Resposta (Async): {response.status_code} ({duration:.2f}s)")
                    response.raise_for_status()
                    return response.json() if response.content else None
                except httpx.HTTPStatusError as e:
                    logger.error(f"Erro HTTP (Async): {e}")
                    raise ApiZenHttpError(str(e), status_code=e.response.status_code, response_data=e.response.text)
                except httpx.RequestError as e:
                    logger.error(f"Erro de rede/timeout (Async): {e}")
                    raise ApiZenError(str(e))

        return await send_async_request()

    async def get(self, endpoint: str, params: dict = None, **kwargs):
        return await self._request("GET", endpoint, params=params, **kwargs)

    async def post(self, endpoint: str, data: dict = None, json: dict = None, **kwargs):
        return await self._request("POST", endpoint, data=data, json=json, **kwargs)

    async def put(self, endpoint: str, data: dict = None, json: dict = None, **kwargs):
        return await self._request("PUT", endpoint, data=data, json=json, **kwargs)

    async def patch(self, endpoint: str, data: dict = None, json: dict = None, **kwargs):
        return await self._request("PATCH", endpoint, data=data, json=json, **kwargs)

    async def delete(self, endpoint: str, **kwargs):
        return await self._request("DELETE", endpoint, **kwargs)

def request_api(api: str):
    """Simplificação extrema para requisições rápidas."""
    return ApiZen().get(api)

