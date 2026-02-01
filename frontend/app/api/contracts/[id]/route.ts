import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const id = (await params).id;
    const response = await fetch(`http://localhost:8000/api/contracts/${id}`);
    const data = await response.json();

    if (!response.ok || data?.success === false) {
      return NextResponse.json(
        { error: data?.detail || data?.error || 'Failed to fetch contract' },
        { status: response.status || 500 }
      );
    }

    return NextResponse.json({
      status: 'success',
      contract: data.contract || null,
      error: null,
    });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to fetch contract' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const id = (await params).id;
    const response = await fetch(`http://localhost:8000/api/contracts/${id}`, {
      method: 'DELETE',
    });
    const data = await response.json();

    if (!response.ok || data?.success === false) {
      return NextResponse.json(
        { error: data?.detail || data?.error || 'Failed to delete contract' },
        { status: response.status || 500 }
      );
    }

    return NextResponse.json({
      status: 'success',
      message: data.message || 'Contract deleted',
      error: null,
    });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to delete contract' },
      { status: 500 }
    );
  }
}
