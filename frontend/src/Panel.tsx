// Import for type checking
import {
  checkPluginVersion,
  type InvenTreePluginContext
} from '@inventreedb/ui';
import { Tabs } from '@mantine/core';
import { Bounds, OrbitControls } from '@react-three/drei';
import { Canvas, type ThreeElements } from '@react-three/fiber';
import { useEffect, useRef, useState } from 'react';
import type * as THREE from 'three';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js';

function STLMesh({
  context,
  ...props
}: { context: InvenTreePluginContext } & ThreeElements['mesh']) {
  const model_color: string = context.context.model_color;

  const meshRef = useRef<THREE.Mesh>(null!);
  console.log(props.geometry);
  return (
    <mesh {...props} ref={meshRef} geometry={props.geometry} scale={1}>
      <meshPhongMaterial
        color={model_color}
        emissive={'#000000'}
        specular={'#000000'}
        shininess={50}
        reflectivity={1}
        refractionRatio={1}
      />
    </mesh>
  );
}

/**
 * Render a custom panel with the provided context.
 * Refer to the InvenTree documentation for the context interface
 * https://docs.inventree.org/en/latest/plugins/mixins/ui/#plugin-context
 */
function STLViewerPanel({ context }: { context: InvenTreePluginContext }) {
  const [geometries, setGeometries] = useState<THREE.BufferGeometry[]>([]);

  const attachment_urls: string[] = context.context.attachments;

  useEffect(() => {
    const loader = new STLLoader();
    Promise.all(
      attachment_urls.map(
        (url) =>
          new Promise<THREE.BufferGeometry>((resolve) => {
            loader.load(url, (geometry) => resolve(geometry));
          })
      )
    ).then(setGeometries);
  }, [attachment_urls]);

  const tab_list = attachment_urls.map((url) => (
    <Tabs.Tab value={url.substring(url.lastIndexOf('/') + 1)}>
      {url.substring(url.lastIndexOf('/') + 1)}
    </Tabs.Tab>
  ));

  const tab_panels = attachment_urls.map((url, index) => (
    <Tabs.Panel value={url.substring(url.lastIndexOf('/') + 1)}>
      <Canvas style={{ height: 500 }}>
        <Bounds fit observe clip>
          <ambientLight />
          <pointLight position={[100, 100, 100]} decay={0} />
          <pointLight position={[-100, -100, -100]} decay={0} />
          <STLMesh context={context} geometry={geometries[index]} />
          <OrbitControls />
        </Bounds>
      </Canvas>
    </Tabs.Panel>
  ));

  return (
    <>
      <Tabs>
        <Tabs.List>{tab_list}</Tabs.List>
        {tab_panels}
      </Tabs>
    </>
  );
}

// This is the function which is called by InvenTree to render the actual panel component
export function renderSTLViewerPanel(context: InvenTreePluginContext) {
  checkPluginVersion(context);

  return <STLViewerPanel context={context} />;
}
