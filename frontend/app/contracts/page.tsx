'use client';

import { useEffect, useMemo, useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Skeleton } from '@/components/ui/skeleton';
import { Trash2, CloudDownload, RefreshCcw } from 'lucide-react';

interface ContractRecord {
  id?: string;
  name?: string;
  title?: string;
  filename?: string;
  file_url?: string;
  type?: string;
  contract_type?: string;
  parties?: string[];
  notes?: string;
  status?: string;
  uploaded_at?: string;
  created_at?: { seconds?: number; nanoseconds?: number } | string;
}

const formatTimestamp = (value?: ContractRecord['created_at'] | ContractRecord['uploaded_at']) => {
  if (!value) return 'Unknown date';
  if (typeof value === 'string') {
    const parsed = new Date(value);
    return Number.isNaN(parsed.getTime()) ? value : parsed.toLocaleString();
  }
  if (typeof value === 'object' && value.seconds) {
    return new Date(value.seconds * 1000).toLocaleString();
  }
  return 'Unknown date';
};

export default function ContractsPage() {
  const [contracts, setContracts] = useState<ContractRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formState, setFormState] = useState({
    name: '',
    contractType: '',
    parties: '',
    notes: '',
    file: null as File | null,
  });

  const fetchContracts = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/contracts');
      const data = await response.json();

      if (!response.ok || data?.status === 'error') {
        throw new Error(data?.error || 'Failed to load contracts');
      }

      setContracts(Array.isArray(data.contracts) ? data.contracts : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load contracts');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchContracts();
  }, []);

  const handleUpload = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!formState.file || !formState.name.trim()) {
      setError('Contract name and PDF file are required.');
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', formState.file);
      formData.append('name', formState.name.trim());

      if (formState.contractType.trim()) {
        formData.append('contract_type', formState.contractType.trim());
      }

      if (formState.parties.trim()) {
        const partiesList = formState.parties
          .split(',')
          .map((party) => party.trim())
          .filter(Boolean);
        formData.append('parties', JSON.stringify(partiesList));
      }

      if (formState.notes.trim()) {
        formData.append('notes', formState.notes.trim());
      }

      const response = await fetch('/api/contracts', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok || data?.status === 'error') {
        throw new Error(data?.error || 'Upload failed');
      }

      setFormState({
        name: '',
        contractType: '',
        parties: '',
        notes: '',
        file: null,
      });

      await fetchContracts();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (contractId?: string) => {
    if (!contractId) return;
    try {
      const response = await fetch(`/api/contracts/${contractId}`, { method: 'DELETE' });
      const data = await response.json();
      if (!response.ok || data?.status === 'error') {
        throw new Error(data?.error || 'Failed to delete contract');
      }
      setContracts((prev) => prev.filter((contract) => (contract.id || contractId) !== contractId));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete contract');
    }
  };

  const handleDownload = async (contractId?: string) => {
    if (!contractId) return;
    try {
      const response = await fetch(`/api/contracts/${contractId}/download`);
      const data = await response.json();
      if (!response.ok || data?.status === 'error' || !data?.download_url) {
        throw new Error(data?.error || 'Failed to get download link');
      }
      window.open(data.download_url, '_blank');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get download link');
    }
  };

  const hasContracts = useMemo(() => contracts.length > 0, [contracts]);

  return (
    <div className="container mx-auto px-4 py-10 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Contracts</h1>
          <p className="text-sm text-muted-foreground">
            Upload and manage contract files for LegalMind analysis.
          </p>
        </div>
        <Button variant="outline" size="sm" onClick={fetchContracts} disabled={isLoading}>
          <RefreshCcw className="mr-2 h-4 w-4" />
          Refresh
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Upload Contract</CardTitle>
          <CardDescription>PDF uploads are stored securely in Cloud Storage.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleUpload} className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="contract-name">Contract name</Label>
              <Input
                id="contract-name"
                value={formState.name}
                onChange={(event) => setFormState((prev) => ({ ...prev, name: event.target.value }))}
                placeholder="Master Services Agreement"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="contract-type">Contract type</Label>
              <Input
                id="contract-type"
                value={formState.contractType}
                onChange={(event) => setFormState((prev) => ({ ...prev, contractType: event.target.value }))}
                placeholder="Services, NDA, SLA"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="contract-parties">Parties (comma-separated)</Label>
              <Input
                id="contract-parties"
                value={formState.parties}
                onChange={(event) => setFormState((prev) => ({ ...prev, parties: event.target.value }))}
                placeholder="Acme Corp, Globex"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="contract-notes">Notes</Label>
              <Input
                id="contract-notes"
                value={formState.notes}
                onChange={(event) => setFormState((prev) => ({ ...prev, notes: event.target.value }))}
                placeholder="Optional context for the legal team"
              />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="contract-file">PDF file</Label>
              <Input
                id="contract-file"
                type="file"
                accept="application/pdf"
                onChange={(event) =>
                  setFormState((prev) => ({
                    ...prev,
                    file: event.target.files ? event.target.files[0] : null,
                  }))
                }
              />
            </div>
            <div className="md:col-span-2 flex items-center justify-between">
              {error ? <p className="text-sm text-destructive">{error}</p> : <span />}
              <Button type="submit" disabled={isUploading}>
                {isUploading ? 'Uploading...' : 'Upload Contract'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Contract Library</CardTitle>
          <CardDescription>{hasContracts ? 'Recent contract uploads.' : 'No contracts uploaded yet.'}</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-2">
              {Array.from({ length: 4 }).map((_, index) => (
                <Skeleton key={index} className="h-10 w-full" />
              ))}
            </div>
          ) : (
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Contract</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Uploaded</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {contracts.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} className="h-24 text-center text-muted-foreground">
                        No contracts found.
                      </TableCell>
                    </TableRow>
                  ) : (
                    contracts.map((contract) => {
                      const contractId = contract.id;
                      return (
                        <TableRow key={contractId || contract.name}>
                          <TableCell>
                            <div className="space-y-1">
                              <p className="font-medium">{contract.name || contract.title || 'Untitled Contract'}</p>
                              <p className="text-xs text-muted-foreground">{contract.filename || 'PDF file'}</p>
                            </div>
                          </TableCell>
                          <TableCell>{contract.contract_type || contract.type || 'Unknown'}</TableCell>
                          <TableCell>
                            <Badge variant="outline">{contract.status || 'uploaded'}</Badge>
                          </TableCell>
                          <TableCell>{formatTimestamp(contract.uploaded_at || contract.created_at)}</TableCell>
                          <TableCell className="text-right space-x-2">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleDownload(contractId)}
                              disabled={!contractId}
                            >
                              <CloudDownload className="mr-2 h-4 w-4" />
                              Download
                            </Button>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => handleDelete(contractId)}
                              disabled={!contractId}
                            >
                              <Trash2 className="mr-2 h-4 w-4" />
                              Delete
                            </Button>
                          </TableCell>
                        </TableRow>
                      );
                    })
                  )}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
