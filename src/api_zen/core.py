import requests
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import time

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ApiZen")

class ApiZen:
    """
    Uma classe facilitadora e robusta para fazer requisições a APIs REST.
    """
    def __init__(self, base_url: str = "", headers: dict = None, timeout: int = 10, max_retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Configuração de Retentativas (Resiliência)
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def set_token(self, token: str, scheme: str = "Bearer"):
        """Define o token de autenticação nos headers."""
        self.session.headers.update({"Authorization": f"{scheme} {token}"})
        logger.info(f"Token de autenticação ({scheme}) configurado.")

    def _get_url(self, endpoint: str) -> str:
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _request(self, method: str, endpoint: str, **kwargs):
        url = self._get_url(endpoint)
        logger.info(f"Chamando {method} em: {url}")
        
        start_time = time.time()
        try:
            kwargs.setdefault("timeout", self.timeout)
            response = self.session.request(method, url, **kwargs)
            duration = time.time() - start_time
            
            logger.info(f"Resposta: {response.status_code} ({duration:.2f}s)")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            raise

    def get(self, endpoint: str, params: dict = None):
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: dict = None, json: dict = None):
        return self._request("POST", endpoint, data=data, json=json)

    def put(self, endpoint: str, data: dict = None, json: dict = None):
        return self._request("PUT", endpoint, data=data, json=json)

    def delete(self, endpoint: str):
        return self._request("DELETE", endpoint)

def request_api(api: str):
    """Mantendo para compatibilidade simples."""
    return ApiZen().get(api)
