-- Tabela principal de vendas
CREATE TABLE vendas (
  id BIGSERIAL PRIMARY KEY,
  id_pagamento TEXT UNIQUE,
  id_ingresso TEXT UNIQUE,
  nome_comprador TEXT,
  email TEXT,
  status TEXT DEFAULT 'pending',
  utilizado BOOLEAN DEFAULT FALSE,
  valor DECIMAL(10,2),
  descricao TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_vendas_status ON vendas(status);
CREATE INDEX idx_vendas_utilizado ON vendas(utilizado);
CREATE INDEX idx_vendas_id_ingresso ON vendas(id_ingresso);

-- Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para atualizar updated_at
CREATE TRIGGER update_vendas_updated_at 
    BEFORE UPDATE ON vendas 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();