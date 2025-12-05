import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Wallet, Mail, Lock, User, Phone, Loader2, AtSign } from 'lucide-react';

export default function Register() {
  const navigate = useNavigate();
  const { register, loading } = useAuth();
  const [formData, setFormData] = useState({
    nome: '',
    username: '',
    email: '',
    senha: '',
    telefone: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    const result = await register(formData);
    
    if (result.success) {
      // Redireciona para login após registro bem-sucedido
      navigate('/login');
    }
    
    setIsSubmitting(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{
      background: 'linear-gradient(135deg, #0a1929 0%, #0f2239 50%, #0a1929 100%)',
    }}>
      <Card className="w-full max-w-md" style={{
        background: 'rgba(15, 34, 57, 0.8)',
        backdropFilter: 'blur(12px)',
        border: '1px solid rgba(16, 185, 129, 0.2)',
      }}>
        <CardHeader className="space-y-1 text-center">
          <div className="flex justify-center mb-4">
            <div className="p-3 rounded-full" style={{
              background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(34, 211, 238, 0.2) 100%)',
            }}>
              <Wallet className="w-8 h-8" style={{ color: '#10b981' }} />
            </div>
          </div>
          <CardTitle className="text-2xl font-bold" style={{
            background: 'linear-gradient(135deg, #10b981 0%, #22d3ee 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}>
            Criar conta
          </CardTitle>
          <CardDescription className="text-gray-400">
            Preencha os dados para começar
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="nome" className="text-gray-300">Nome completo</Label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  id="nome"
                  type="text"
                  placeholder="Seu nome"
                  value={formData.nome}
                  onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                  required
                  minLength={2}
                  className="pl-10"
                  style={{
                    background: 'rgba(10, 25, 41, 0.6)',
                    border: '1px solid rgba(16, 185, 129, 0.2)',
                    color: '#e0e7ff',
                  }}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="username" className="text-gray-300">Nome de usuário</Label>
              <div className="relative">
                <AtSign className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  id="username"
                  type="text"
                  placeholder="stark, luan, etc."
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value.toLowerCase().replace(/\s+/g, '') })}
                  required
                  minLength={3}
                  className="pl-10"
                  style={{
                    background: 'rgba(10, 25, 41, 0.6)',
                    border: '1px solid rgba(16, 185, 129, 0.2)',
                    color: '#e0e7ff',
                  }}
                />
              </div>
              <p className="text-xs text-gray-500">Mínimo 3 caracteres, sem espaços</p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="email" className="text-gray-300">Email</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  id="email"
                  type="email"
                  placeholder="seu@email.com"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                  className="pl-10"
                  style={{
                    background: 'rgba(10, 25, 41, 0.6)',
                    border: '1px solid rgba(16, 185, 129, 0.2)',
                    color: '#e0e7ff',
                  }}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="senha" className="text-gray-300">Senha</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  id="senha"
                  type="password"
                  placeholder="Mínimo 6 caracteres"
                  value={formData.senha}
                  onChange={(e) => setFormData({ ...formData, senha: e.target.value })}
                  required
                  minLength={6}
                  className="pl-10"
                  style={{
                    background: 'rgba(10, 25, 41, 0.6)',
                    border: '1px solid rgba(16, 185, 129, 0.2)',
                    color: '#e0e7ff',
                  }}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="telefone" className="text-gray-300">Telefone (opcional)</Label>
              <div className="relative">
                <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  id="telefone"
                  type="tel"
                  placeholder="(11) 99999-9999"
                  value={formData.telefone}
                  onChange={(e) => setFormData({ ...formData, telefone: e.target.value })}
                  className="pl-10"
                  style={{
                    background: 'rgba(10, 25, 41, 0.6)',
                    border: '1px solid rgba(16, 185, 129, 0.2)',
                    color: '#e0e7ff',
                  }}
                />
              </div>
            </div>

            <Button
              type="submit"
              className="w-full"
              disabled={isSubmitting || loading}
              style={{
                background: 'linear-gradient(135deg, #10b981 0%, #22d3ee 100%)',
                color: '#0a1929',
                fontWeight: '600',
              }}
            >
              {isSubmitting || loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Criando conta...
                </>
              ) : (
                'Criar conta'
              )}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-400">
              Já tem uma conta?{' '}
              <Link
                to="/login"
                className="font-medium hover:underline"
                style={{ color: '#10b981' }}
              >
                Fazer login
              </Link>
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}


