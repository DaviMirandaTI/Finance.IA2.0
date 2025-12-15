import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Download, Calendar } from "lucide-react";
import { toast } from "sonner";
import { listarFaturasCompletas, exportarFaturaCSV, listarCartoes } from "@/lib/api";

export default function FaturasCartao() {
  const { cartaoId } = useParams();
  const navigate = useNavigate();
  const [faturas, setFaturas] = useState([]);
  const [cartao, setCartao] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    carregarDados();
  }, [cartaoId]);

  const carregarDados = async () => {
    try {
      setLoading(true);
      
      // Buscar cartão
      const cartoes = await listarCartoes();
      const cartaoEncontrado = cartoes.find(c => c.id === cartaoId);
      setCartao(cartaoEncontrado);
      
      // Buscar faturas (incluindo futuras)
      const faturasData = await listarFaturasCompletas(cartaoId, true);
      setFaturas(faturasData || []);
    } catch (error) {
      console.error("Erro ao carregar faturas:", error);
      toast.error("Erro ao carregar faturas do cartão");
    } finally {
      setLoading(false);
    }
  };

  const handleExportar = async (mesReferencia) => {
    try {
      await exportarFaturaCSV(cartaoId, mesReferencia);
      toast.success("Fatura exportada com sucesso!");
    } catch (error) {
      console.error("Erro ao exportar:", error);
      toast.error("Erro ao exportar fatura");
    }
  };

  const formatarData = (dataStr) => {
    if (!dataStr) return "-";
    try {
      return new Date(dataStr + "T00:00:00").toLocaleDateString("pt-BR");
    } catch {
      return dataStr;
    }
  };

  const formatarMes = (mesStr) => {
    if (!mesStr) return "-";
    try {
      const [ano, mes] = mesStr.split("-");
      const meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
      ];
      return `${meses[parseInt(mes) - 1]} ${ano}`;
    } catch {
      return mesStr;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-slate-400">Carregando...</p>
      </div>
    );
  }

  return (
    <div
      className="min-h-screen w-full flex flex-col items-center px-4 py-8"
      style={{
        background:
          "radial-gradient(circle at top, rgba(16,185,129,0.15), transparent 55%), #020617",
      }}
    >
      <div className="w-full max-w-5xl space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <Button
            variant="ghost"
            onClick={() => navigate(-1)}
            className="text-slate-300 hover:text-slate-50 hover:bg-slate-800"
          >
            <ArrowLeft size={20} className="mr-2" />
            Voltar
          </Button>
        </div>

        {/* Título */}
        <Card className="bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur">
          <CardHeader>
            <CardTitle className="text-slate-50 text-xl">
              Faturas do Cartão: {cartao?.nome || "Cartão"}
            </CardTitle>
            {cartao && (
              <p className="text-xs text-slate-400 mt-1">
                Limite: R$ {cartao.limite_total.toFixed(2)} | 
                Disponível: R$ {cartao.limite_disponivel.toFixed(2)}
              </p>
            )}
          </CardHeader>
        </Card>

        {/* Lista de Faturas */}
        {faturas.length === 0 ? (
          <Card className="bg-slate-900/80 border border-slate-800">
            <CardContent className="py-8 text-center">
              <p className="text-slate-400">Nenhuma fatura encontrada</p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {faturas.map((fatura) => (
              <Card
                key={fatura.id}
                className={`bg-slate-900/80 border shadow-xl backdrop-blur ${
                  fatura.status === "futura"
                    ? "border-blue-500/50"
                    : fatura.status === "vencida"
                    ? "border-red-500/50"
                    : "border-slate-800"
                }`}
              >
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-slate-50 text-lg">
                        {formatarMes(fatura.mes_referencia)}
                      </CardTitle>
                      <div className="flex items-center gap-2 mt-2">
                        <Badge
                          variant={
                            fatura.status === "futura"
                              ? "default"
                              : fatura.status === "paga"
                              ? "default"
                              : "destructive"
                          }
                          className={
                            fatura.status === "futura"
                              ? "bg-blue-500/20 text-blue-300 border-blue-500/50"
                              : fatura.status === "paga"
                              ? "bg-green-500/20 text-green-300 border-green-500/50"
                              : ""
                          }
                        >
                          {fatura.status === "futura"
                            ? "Futura"
                            : fatura.status === "paga"
                            ? "Paga"
                            : fatura.status === "vencida"
                            ? "Vencida"
                            : "Aberta"}
                        </Badge>
                        {fatura.status === "futura" && (
                          <Badge variant="outline" className="text-xs border-blue-500/30 text-blue-300">
                            <Calendar size={12} className="mr-1" />
                            Projetada
                          </Badge>
                        )}
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-slate-50">
                        R$ {fatura.valor_total.toFixed(2)}
                      </p>
                      {fatura.data_vencimento && (
                        <p className="text-xs text-slate-400 mt-1">
                          Venc: {formatarData(fatura.data_vencimento)}
                        </p>
                      )}
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-slate-400">
                        {fatura.lancamentos?.length || fatura.lancamentos_ids?.length || 0}{" "}
                        lançamento(s)
                      </p>
                    </div>
                    <Button
                      onClick={() => handleExportar(fatura.mes_referencia)}
                      variant="outline"
                      size="sm"
                      className="border-emerald-500/50 text-emerald-300 hover:bg-emerald-500/10"
                    >
                      <Download size={16} className="mr-2" />
                      Exportar CSV
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

